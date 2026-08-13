import json
import logging
import os
import time

from dotenv import load_dotenv

load_dotenv()  # must run before any module that reads env vars at import time

import uvicorn
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from graph import run_query, stream_query
from llm import llm
from models import (
    AuthResponse,
    ConversationListResponse,
    ConversationSummary,
    DocumentListResponse,
    IngestResponse,
    LoginRequest,
    MessageItem,
    MessagesResponse,
    QueryRequest,
    QueryResponse,
    RegisterRequest,
    RegisterResponse,
    RetrievalPassage,
    RetrieveRequest,
    RetrieveResponse,
    SchemaResponse,
    SQLIngestResponse,
    UpdateProfileRequest,
)
from Observability.langfuse_client import observe_span
from Services.Auth_Service import (
    authenticate_with_auth0,
    get_current_user,
    register_user,
    update_user_profile,
)
from Services.Conversation_Service import (
    add_message,
    create_conversation,
    delete_conversation,
    get_messages,
    list_conversations,
    maybe_set_title_from_first_message,
)
from Services.Guardrail_Service import check_guardrails
from Services.Ollama_Router_Service import classify_and_maybe_answer
from Services.RAG_Service import DOCUMENTS_DIR, SUPPORTED_EXTENSIONS, rag_service
from Services.SLO_Metrics_Service import (
    get_aggregated_slo_metrics,
    record_guardrail_block,
    record_query_metric,
    reset_slo_metrics,
)
from Services.SQL_Service import (
    get_schema_description,
    ingest_sql_content,
    ingest_sql_file,
    list_tables,
)

SQL_UPLOAD_DIR = os.getenv("SQL_UPLOAD_DIR", "./data/sql_uploads")


# Suppress Azure HTTP request/response logs
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
    logging.WARNING
)

logger = logging.getLogger("finance_workflow")
logging.basicConfig(level=getattr(logging, llm.LOG_LEVEL, logging.INFO))


app = FastAPI(
    title="Finance Risk & Investment Intelligent System",
    description=(
        "AI-powered multi-agent system for financial risk analysis, "
        "investment performance evaluation, and regulatory exposure "
        "assessment."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


@app.get("/slo/metrics", tags=["Metrics"])
def get_slo_metrics():
    return get_aggregated_slo_metrics()


@app.post("/slo/reset", tags=["Metrics"])
def reset_slo():
    return reset_slo_metrics()


@app.post("/auth/register", response_model=RegisterResponse, tags=["Auth"])
def register(request: RegisterRequest):
    res = register_user(
        name=request.name, email=request.email, password=request.password
    )
    return RegisterResponse(
        message=res["message"],
        email=res["email"],
        requires_verification=res["requires_verification"],
    )


@app.post("/auth/login", response_model=AuthResponse, tags=["Auth"])
def login(request: LoginRequest):
    res = authenticate_with_auth0(request.username, request.password)
    return AuthResponse(
        access_token=res["access_token"],
        username=res["username"],
        email=request.username,
    )


@app.post("/auth/profile/update", tags=["Auth"])
def update_profile(
    request: UpdateProfileRequest, current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("id") or current_user.get("raw_claims", {}).get("sub")
    res = update_user_profile(
        user_id=user_id,
        name=request.name,
        old_password=request.old_password,
        new_password=request.new_password,
    )
    return res


@app.post("/query", response_model=QueryResponse, tags=["Search"])
def handle_query(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty.")
    if not request.conversation_id:
        raise HTTPException(status_code=400, detail="conversation_id is required.")

    add_message(request.conversation_id, current_user["id"], "user", request.query)
    maybe_set_title_from_first_message(
        request.conversation_id, current_user["id"], request.query
    )

    # ---- 1. Input Guardrails Check ----
    has_docs = len(rag_service.list_documents()) > 0
    has_sqls = len(list_tables()) > 0
    guard_res = check_guardrails(
        request.query, has_documents=has_docs, has_tables=has_sqls
    )
    if guard_res.is_blocked:
        record_guardrail_block(request.query)
        logger.warning("Query blocked by guardrail: %s", guard_res.category)
        response = QueryResponse(
            status="blocked",
            final_response=guard_res.reply,
            message=f"Blocked by guardrail ({guard_res.category}).",
            route="guardrail",
        )
        add_message(
            request.conversation_id,
            current_user["id"],
            "assistant",
            response.final_response,
        )
        return response

    with observe_span(
        "http_query",
        input_data={"query": request.query},
        metadata={"provider": "http", "endpoint": "/query"},
        as_type="chain",
        provider="http",
    ) as span:
        routing = classify_and_maybe_answer(request.query)
        if routing["classification"] == "simple":
            logger.info("Ollama pre-router: SIMPLE - answered directly, crew skipped.")
            response = QueryResponse(
                status="completed",
                final_response=routing["answer"],
                message="Answered directly (simple query, crew skipped).",
                route="direct",
            )
            add_message(
                request.conversation_id,
                current_user["id"],
                "assistant",
                response.final_response,
            )
            if span is not None:
                span.update(
                    output={
                        "status": response.status,
                        "final_response": response.final_response,
                        "message": response.message,
                    },
                    metadata={
                        "provider": "http",
                        "endpoint": "/query",
                        "used_provider": "ollama",
                        "classification": routing["classification"],
                    },
                )
            record_query_metric(
                request.query,
                latency_sec=0.45,
                router_sec=0.35,
                confidence=0.85,
                revisions=0,
                status="completed",
                route="direct",
            )
            return response

        try:
            final_state = run_query(request.query)
        except Exception as e:
            logger.exception("Workflow execution failed")
            err_text = str(e)
            if (
                "(content_filter)" in err_text
                or "ResponsibleAIPolicyViolation" in err_text
                or "content_filter" in err_text
            ):
                record_guardrail_block(request.query)
                blocked_response = "This query was blocked by content safety policy and cannot be processed."
                add_message(
                    request.conversation_id,
                    current_user["id"],
                    "assistant",
                    blocked_response,
                )
                return QueryResponse(
                    status="blocked",
                    final_response=blocked_response,
                    message="Blocked by content safety policy.",
                    route="guardrail",
                )
            raise HTTPException(
                status_code=500, detail=f"Workflow execution failed: {e}"
            )

        final_route = final_state.get("route", "crew")
        if final_route in ("final", "revise"):
            final_route = "crew"
        elif final_route == "human_handoff":
            final_route = "escalated"

        response = QueryResponse(
            status=final_state.get("status", "completed"),
            final_response=final_state.get("final_response", ""),
            message="Working as Expected...",
            route=final_route,
            confidence=final_state.get("confidence"),
        )
        add_message(
            request.conversation_id,
            current_user["id"],
            "assistant",
            response.final_response,
        )
        if span is not None:
            span.update(
                output={
                    "status": response.status,
                    "final_response": response.final_response,
                    "message": response.message,
                },
                metadata={
                    "provider": "http",
                    "endpoint": "/query",
                    "used_provider": "crew",
                    "classification": routing["classification"],
                },
            )
        return response


@app.post("/query/stream", tags=["Search"])
def handle_query_stream(
    request: QueryRequest, current_user: dict = Depends(get_current_user)
):
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty.")
    if not request.conversation_id:
        raise HTTPException(status_code=400, detail="conversation_id is required.")

    add_message(request.conversation_id, current_user["id"], "user", request.query)
    maybe_set_title_from_first_message(
        request.conversation_id, current_user["id"], request.query
    )

    # ---- 1. Input Guardrails Check ----
    has_docs = len(rag_service.list_documents()) > 0
    has_sqls = len(list_tables()) > 0
    guard_res = check_guardrails(
        request.query, has_documents=has_docs, has_tables=has_sqls
    )

    if guard_res.is_blocked:
        record_guardrail_block(request.query)

        def guardrail_event_generator():
            logger.warning("Query stream blocked by guardrail: %s", guard_res.category)
            payload = {
                "phase": "final_response",
                "final_response": guard_res.reply,
                "status": "blocked",
                "confidence": None,
                "revise_count": 0,
                "route": "guardrail_blocked",
            }
            add_message(
                request.conversation_id,
                current_user["id"],
                "assistant",
                guard_res.reply,
            )
            yield f"data: {json.dumps(payload)}\n\n"
            yield "event: done\ndata: {}\n\n"

        return StreamingResponse(
            guardrail_event_generator(), media_type="text/event-stream"
        )

    routing = classify_and_maybe_answer(request.query)

    def event_generator():
        start_time = time.time()
        if routing["classification"] == "simple":
            logger.info("Ollama pre-router: SIMPLE - answered directly, crew skipped.")
            record_query_metric(
                request.query, latency_sec=0.45, router_sec=0.35, route="direct"
            )
            payload = {
                "phase": "final_response",
                "final_response": routing["answer"],
                "status": "completed",
                "confidence": None,
                "revise_count": 0,
                "route": "direct",
            }
            add_message(
                request.conversation_id,
                current_user["id"],
                "assistant",
                routing["answer"],
            )
            yield f"data: {json.dumps(payload)}\n\n"
            yield "event: done\ndata: {}\n\n"
            return

        try:
            last_answer = ""
            last_conf = 0.85
            last_retries = 0
            for phase, payload in stream_query(request.query):
                if payload.get("final_response"):
                    last_answer = payload["final_response"]
                if payload.get("confidence") is not None:
                    last_conf = payload["confidence"]
                if payload.get("revise_count") is not None:
                    last_retries = payload["revise_count"]
                yield f"data: {json.dumps({'phase': phase, **payload})}\n\n"

            t_delta = round(time.time() - start_time, 2)
            record_query_metric(
                request.query,
                latency_sec=t_delta,
                router_sec=0.40,
                confidence=last_conf,
                revisions=last_retries,
                route="crew",
            )
            add_message(
                request.conversation_id, current_user["id"], "assistant", last_answer
            )
        except Exception as e:
            logger.exception("Workflow stream execution failed")
            err_text = str(e)
            if (
                "(content_filter)" in err_text
                or "ResponsibleAIPolicyViolation" in err_text
                or "content_filter" in err_text
            ):
                record_guardrail_block()
                blocked_response = "This query was blocked by content safety policy and cannot be processed."
                add_message(
                    request.conversation_id,
                    current_user["id"],
                    "assistant",
                    blocked_response,
                )
                err_payload = {
                    "phase": "final_response",
                    "final_response": blocked_response,
                    "status": "blocked",
                    "route": "guardrail",
                }
            else:
                err_payload = {
                    "phase": "final_response",
                    "final_response": f"Workflow failed: {e}",
                    "status": "error",
                }
            yield f"data: {json.dumps(err_payload)}\n\n"

        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ---- CHANGED: now requires auth ----
@app.post("/rag/ingest", response_model=IngestResponse, tags=["RAG"])
async def ingest_document(
    file: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}",
        )

    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    dest_path = os.path.join(DOCUMENTS_DIR, file.filename)

    try:
        content = await file.read()
        with open(dest_path, "wb") as f:
            f.write(content)
        chunks = rag_service.ingest_file(dest_path)
    except Exception as e:
        logger.exception("Ingestion failed")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

    return IngestResponse(
        filename=file.filename,
        chunks_ingested=chunks,
        total_documents=len(rag_service.list_documents()),
        message=f"'{file.filename}' indexed successfully.",
    )


# ---- CHANGED: now requires auth ----
@app.post("/rag/retrieve", response_model=RetrieveResponse, tags=["RAG"])
def retrieve_documents(
    request: RetrieveRequest, current_user: dict = Depends(get_current_user)
):
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty.")
    results = rag_service.search(request.query, k=request.top_k)
    return RetrieveResponse(
        query=request.query,
        results=[RetrievalPassage(**r) for r in results],
    )


# ---- CHANGED: now requires auth ----
@app.get("/rag/documents", response_model=DocumentListResponse, tags=["RAG"])
def list_documents(current_user: dict = Depends(get_current_user)):
    return DocumentListResponse(documents=rag_service.list_documents())


# ---- CHANGED: now requires auth ----
@app.delete(
    "/rag/documents/{filename}", response_model=DocumentListResponse, tags=["RAG"]
)
def delete_document(filename: str, current_user: dict = Depends(get_current_user)):
    removed = rag_service.remove_file(filename)
    if not removed:
        raise HTTPException(status_code=404, detail=f"Document '{filename}' not found.")
    return DocumentListResponse(documents=rag_service.list_documents())


# ---- CHANGED: now requires auth ----
@app.post("/sql/ingest", response_model=SQLIngestResponse, tags=["SQL"])
async def ingest_sql(
    file: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    if not file.filename.lower().endswith(".sql"):
        raise HTTPException(status_code=400, detail="Only .sql files are supported.")

    try:
        content_bytes = await file.read()
        sql_text = content_bytes.decode("utf-8-sig", errors="replace")
    except Exception as e:
        logger.exception("Failed to read uploaded SQL file content")
        raise HTTPException(status_code=400, detail=f"Could not read SQL file: {e}")

    # Optional local save (safe fallback if disk is read-only)
    try:
        os.makedirs(SQL_UPLOAD_DIR, exist_ok=True)
        dest_path = os.path.join(SQL_UPLOAD_DIR, file.filename)
        with open(dest_path, "wb") as f:
            f.write(content_bytes)
    except Exception as e:
        logger.warning(
            "Could not write uploaded SQL file to local disk (likely serverless/read-only environment): %s",
            e,
        )

    try:
        result = ingest_sql_content(sql_text)
    except Exception as e:
        logger.exception("SQL ingestion failed")
        raise HTTPException(status_code=500, detail=f"SQL ingestion failed: {e}")

    return SQLIngestResponse(
        tables=result["tables"],
        message=f"'{file.filename}' ingested successfully.",
    )


# ---- CHANGED: now requires auth ----
@app.get("/sql/schema", response_model=SchemaResponse, tags=["SQL"])
def get_sql_schema(current_user: dict = Depends(get_current_user)):
    return SchemaResponse(
        tables=list_tables(), schema_description=get_schema_description()
    )


# ---------------------------------------------------------------------
# Conversations
# ---------------------------------------------------------------------


@app.post("/conversations", response_model=ConversationSummary, tags=["SessionID"])
def new_conversation(current_user: dict = Depends(get_current_user)):
    conv = create_conversation(current_user["id"])
    return ConversationSummary(
        id=str(conv["id"]),
        title=conv["title"],
        created_at=conv["created_at"].isoformat(),
        updated_at=conv["updated_at"].isoformat(),
    )


@app.get("/conversations", response_model=ConversationListResponse, tags=["SessionID"])
def get_conversations(current_user: dict = Depends(get_current_user)):
    convs = list_conversations(current_user["id"])
    return ConversationListResponse(
        conversations=[
            ConversationSummary(
                id=str(c["id"]),
                title=c["title"],
                created_at=c["created_at"].isoformat(),
                updated_at=c["updated_at"].isoformat(),
            )
            for c in convs
        ]
    )


@app.get(
    "/conversations/{conversation_id}/messages",
    response_model=MessagesResponse,
    tags=["SessionID"],
)
def get_conversation_messages(
    conversation_id: str, current_user: dict = Depends(get_current_user)
):
    msgs = get_messages(conversation_id, current_user["id"])
    if msgs is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return MessagesResponse(
        messages=[
            MessageItem(
                role=m["role"],
                content=m["content"],
                created_at=m["created_at"].isoformat(),
            )
            for m in msgs
        ]
    )


@app.delete("/conversations/{conversation_id}", tags=["SessionID"])
def remove_conversation(
    conversation_id: str, current_user: dict = Depends(get_current_user)
):
    deleted = delete_conversation(conversation_id, current_user["id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return {"deleted": True}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
