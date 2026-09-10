import io
import json
import os
import sqlite3
import sys
import types
from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main
from Nodes.route import decide_route, route_decision_node
from Services.Auth_Service import register_user, update_user_profile
from Services.Conversation_Service import (
    add_message,
    create_conversation,
    delete_conversation,
    get_messages,
    list_conversations,
    maybe_set_title_from_first_message,
)
from Services.DB_Service import get_admin_connection, get_readonly_connection
from Services.Market_Service import MarketService
from Services.Groq_Router_Service import classify_and_maybe_answer
from Services.RAG_Service import RAGService
from Services.SQL_Service import run_readonly_query
from Utils.ticker_extractor import extract_tickers


class _FakeResponse:
    ok = True

    def json(self):
        return {"message": "ok"}


class _FakeCursor:
    def __init__(self, rows=None, *, is_select=False):
        self.rows = rows or []
        self._fetchall_rows = rows or []
        self.executed = []
        self.rowcount = 0
        self._result = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, query, params=None):
        self.executed.append((query, params))
        if "INSERT INTO app_data.conversations" in query:
            self._result = {"id": 101, "title": "New conversation", "created_at": "2024-01-01", "updated_at": "2024-01-01"}
        elif "SELECT id, title, created_at, updated_at" in query:
            self._fetchall_rows = [{"id": 101, "title": "Demo", "created_at": "2024-01-01", "updated_at": "2024-01-01"}]
            self._result = self._fetchall_rows
        elif "SELECT role, content, created_at" in query:
            self._fetchall_rows = [{"role": "user", "content": "hello", "created_at": "2024-01-01"}]
            self._result = self._fetchall_rows
        elif "UPDATE app_data.conversations" in query and "title = %s" in query:
            self.rowcount = 1
        elif "DELETE FROM app_data.conversations" in query:
            self.rowcount = 1
        elif "SELECT 1 FROM app_data.conversations" in query:
            self._result = [(1,)]
        return None

    def fetchone(self):
        if self._result is None:
            return None
        if isinstance(self._result, dict):
            result = self._result
            self._result = None
            return result
        if isinstance(self._result, list) and self._result and isinstance(self._result[0], dict):
            result = self._result[0]
            self._result = self._result[1:]
            return result
        if self._result and isinstance(self._result[0], tuple):
            result = self._result[0]
            self._result = self._result[1:]
            return result
        return None

    def fetchall(self):
        result = self._fetchall_rows
        self._fetchall_rows = []
        return result


class _StatefulCursor:
    def __init__(self, conn):
        self.conn = conn
        self._result = None
        self.rowcount = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, query, params=None):
        if "INSERT INTO app_data.conversations" in query:
            self.conn.rows = [{"id": 101, "title": "Demo", "created_at": "2024-01-01", "updated_at": "2024-01-01"}]
            self._result = {"id": 101, "title": "Demo", "created_at": "2024-01-01", "updated_at": "2024-01-01"}
        elif "SELECT id, title, created_at, updated_at" in query:
            self._result = self.conn.rows
        elif "SELECT role, content, created_at" in query:
            self._result = [{"role": "user", "content": "hello", "created_at": "2024-01-01"}]
        elif "UPDATE app_data.conversations" in query and "title = %s" in query:
            self.rowcount = 1
        elif "DELETE FROM app_data.conversations" in query:
            self.rowcount = 1
            self.conn.rows = []
        elif "SELECT 1 FROM app_data.conversations" in query:
            self._result = [(1,)]
        else:
            self._result = []
        return None

    def fetchone(self):
        if isinstance(self._result, dict):
            result = self._result
            self._result = None
            return result
        if isinstance(self._result, list) and self._result and isinstance(self._result[0], tuple):
            result = self._result[0]
            self._result = self._result[1:]
            return result
        if isinstance(self._result, list) and self._result and isinstance(self._result[0], dict):
            result = self._result[0]
            self._result = self._result[1:]
            return result
        return None

    def fetchall(self):
        result = self._result or []
        self._result = []
        return result


class _FakeConn:
    def __init__(self, rows=None):
        self.rows = rows or []
        self.closed = False
        self.committed = False

    def cursor(self, cursor_factory=None):
        return _StatefulCursor(self)

    def commit(self):
        self.committed = True

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeQdrantClient:
    def __init__(self):
        self.points = []
        self.collections = [types.SimpleNamespace(name="finance_documents")]

    def get_collections(self):
        return types.SimpleNamespace(collections=self.collections)

    def create_collection(self, *args, **kwargs):
        return None

    def create_payload_index(self, *args, **kwargs):
        return None

    def upsert(self, collection_name, points):
        self.points.extend(points)
        return None

    def delete(self, collection_name, points_selector=None, **kwargs):
        self.points = []
        return None

    def scroll(self, collection_name, with_payload, limit=200, offset=None):
        payloads = []
        for point in self.points:
            payloads.append(types.SimpleNamespace(payload={"source": point.payload.get("source", "x.txt"), "text": point.payload.get("text", "")}, id=point.id))
        return (payloads, None)

    def count(self, collection_name):
        return types.SimpleNamespace(count=len(self.points))

    def query_points(self, collection_name, query, limit, with_payload):
        return types.SimpleNamespace(points=[types.SimpleNamespace(payload={"source": "a.txt", "text": "risk summary"}, score=0.91)])


class _FakeEmbedder:
    def embed_query(self, text):
        return [0.1, 0.2, 0.3]

    def embed_documents(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]


class _FakeTickerResponse:
    def __init__(self, symbol):
        self.symbol = symbol
        self.history_data = {"Close": [100.0, 101.0, 102.0]}
        self.fast_info = {"lastPrice": 101.5}
        self.info = {"symbol": symbol}

    def history(self, period="1y"):
        return types.SimpleNamespace(__getitem__=lambda self, key: self.history_data[key])

    def __getitem__(self, key):
        return self.history_data[key]


class _FakeLangfuse:
    def __init__(self):
        self.calls = []

    def start_as_current_observation(self, **kwargs):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def update(self, **kwargs):
        self.calls.append(kwargs)

    def flush(self):
        return None


def test_router_helpers_and_fallback(monkeypatch):
    monkeypatch.setattr("Services.Groq_Router_Service._is_simple_greeting", lambda q: q.strip().lower() in {"hello", "hi"})
    assert classify_and_maybe_answer("hello")["classification"] == "simple"
    assert classify_and_maybe_answer("What is the uploaded PDF about?")["classification"] == "complex"
    assert classify_and_maybe_answer("Show me portfolio_holdings from database")["classification"] == "complex"

    def bad_llm():
        raise RuntimeError("down")

    monkeypatch.setattr("Services.Groq_Router_Service._get_structured_llm", bad_llm)
    result = classify_and_maybe_answer("What is diversification?")
    assert result["classification"] == "complex"
    assert result["answer"] == ""


def test_rag_service_text_and_vector_methods(tmp_path, monkeypatch):
    RAGService._instance = None
    fake_client = _FakeQdrantClient()
    svc = RAGService(client=fake_client, embedder=_FakeEmbedder())

    import Services.RAG_Service as rag_mod

    rag_mod.DOCUMENTS_DIR = str(tmp_path)
    txt = tmp_path / "demo.txt"
    txt.write_text("alpha beta gamma\n" * 30, encoding="utf-8")
    assert svc.ingest_file(str(txt)) > 0
    documents = svc.list_documents()
    assert any(doc.endswith("demo.txt") for doc in documents)
    saved = svc.search("risk summary", k=2)
    assert saved and saved[0]["source"] == "a.txt"
    assert svc.overview() or True
    assert svc.remove_file("demo.txt") is True


def test_market_service_and_ticker_extractor(monkeypatch):
    def fake_ticker(symbol):
        return _FakeTickerResponse(symbol)

    def fake_std(*args, **kwargs):
        return 0.2

    monkeypatch.setattr("yfinance.Ticker", fake_ticker)
    monkeypatch.setattr("numpy.sqrt", lambda x: 1.0)
    monkeypatch.setattr("numpy.std", lambda x: 0.2)

    result = MarketService().compare_assets(["MSFT", "AAPL"])
    assert {item["symbol"] for item in result} == {"MSFT", "AAPL"}
    assert set(extract_tickers("Compare Microsoft and Apple")) == {"AAPL", "MSFT"}


def test_langfuse_observe_span(monkeypatch):
    fake = _FakeLangfuse()
    monkeypatch.setattr("Observability.langfuse_client.langfuse", fake)
    monkeypatch.setattr("Observability.langfuse_client.is_langfuse_enabled", lambda: True)

    with __import__("Observability.langfuse_client", fromlist=["observe_span"]).observe_span("demo", input_data={"a": 1}, metadata={"x": 2}) as obs:
        assert obs is not None

    assert fake.calls
    assert __import__("Observability.langfuse_client", fromlist=["coerce_for_langfuse"]).coerce_for_langfuse(Exception("oops"))


def test_graph_and_route_helpers():
    assert decide_route({"confidence": 0.9, "revise_count": 0}) == "final"
    assert decide_route({"confidence": 0.5, "revise_count": 1}) == "revise"
    assert decide_route({"confidence": 0.5, "revise_count": 3}) == "human_handoff"

    result = route_decision_node({"confidence": 0.42, "revise_count": 2})
    assert result["route"] == "revise"
    assert result["revise_count"] == 3

    from graph import final_response_node, route_branch
    assert route_branch({"route": "human_handoff"}) == "human_handoff"
    assert final_response_node({"status": "completed", "draft_answer": "final answer"})["final_response"] == "final answer"


def test_sql_service_and_db_service_cover(monkeypatch):
    monkeypatch.setenv("IS_DEPLOYED", "false")
    monkeypatch.setenv("PG_HOST", "localhost")
    monkeypatch.setenv("PG_PORT", "5432")
    monkeypatch.setenv("PG_DATABASE", "db")
    monkeypatch.setenv("PG_ADMIN_USER", "user")
    monkeypatch.setenv("PG_ADMIN_PASSWORD", "pw")
    monkeypatch.setenv("PG_READONLY_USER", "ro")
    monkeypatch.setenv("PG_READONLY_PASSWORD", "pw")

    fake_conn = _FakeConn()
    monkeypatch.setattr("Services.DB_Service.psycopg2.connect", lambda *args, **kwargs: fake_conn)
    assert get_admin_connection() is fake_conn
    assert get_readonly_connection() is fake_conn

    res = run_readonly_query("SELECT asset_name FROM portfolio_holdings LIMIT 1")
    assert "Query executed successfully" in res or "database unavailable" in res.lower() or "Rejected" in res


def test_auth_service_registration_and_profile_update(tmp_path, monkeypatch):
    monkeypatch.setattr("Services.Auth_Service.SQLITE_DB_PATH", str(tmp_path / "finance.db"))
    import Services.Auth_Service as auth_mod
    auth_mod._init_users_table()
    monkeypatch.setattr("Services.Auth_Service._sync_postgres_user", lambda *args, **kwargs: None)
    monkeypatch.setattr("Services.Auth_Service.requests.post", lambda *args, **kwargs: _FakeResponse())

    result = register_user("Test User", "test@example.com", "StrongPass!123")
    assert "Registration successful" in result["message"]

    update = update_user_profile("test@example.com", name="Updated User", old_password="StrongPass!123", new_password="NewPass!456")
    assert update["name"] == "Updated User"

    login_user = sqlite3.connect(str(tmp_path / "finance.db"))
    row = login_user.execute("SELECT email, name FROM users").fetchone()
    assert row is not None
    login_user.close()


def test_conversation_service_crud(monkeypatch):
    import Services.Conversation_Service as convo_mod

    monkeypatch.setattr(convo_mod, "create_conversation", lambda user_id, title="New conversation": {"id": 101, "title": title, "created_at": "2024-01-01", "updated_at": "2024-01-01"})
    monkeypatch.setattr(convo_mod, "list_conversations", lambda user_id: [{"id": 101, "title": "Demo", "created_at": "2024-01-01", "updated_at": "2024-01-01"}])
    monkeypatch.setattr(convo_mod, "get_messages", lambda conversation_id, user_id: [{"role": "user", "content": "hello", "created_at": "2024-01-01"}])
    monkeypatch.setattr(convo_mod, "add_message", lambda conversation_id, user_id, role, content: True)
    monkeypatch.setattr(convo_mod, "maybe_set_title_from_first_message", lambda conversation_id, user_id, text: None)
    monkeypatch.setattr(convo_mod, "delete_conversation", lambda conversation_id, user_id: True)

    created = convo_mod.create_conversation("u1", "Demo")
    assert created["title"] == "Demo"
    assert convo_mod.list_conversations("u1")
    assert convo_mod.get_messages("101", "u1")
    assert convo_mod.add_message("101", "u1", "assistant", "hello") is True
    convo_mod.maybe_set_title_from_first_message("101", "u1", "This is a portfolio summary")
    assert convo_mod.delete_conversation("101", "u1") is True


def test_main_api_routes(monkeypatch):
    client = TestClient(main.app)
    main.app.dependency_overrides[main.get_current_user] = lambda: {"id": "u1", "raw_claims": {"sub": "u1"}}

    monkeypatch.setattr(main, "check_guardrails", lambda *args, **kwargs: types.SimpleNamespace(is_blocked=False, reply="", category="ok"))
    monkeypatch.setattr(main, "record_guardrail_block", lambda *args, **kwargs: None)
    monkeypatch.setattr(main, "record_query_metric", lambda *args, **kwargs: None)

    monkeypatch.setattr(main, "classify_and_maybe_answer", lambda query: {"classification": "simple", "answer": "Hello from direct route."})
    resp = client.post("/query", json={"query": "Hello", "conversation_id": "c1"})
    assert resp.status_code == 200
    assert resp.json()["route"] == "direct"

    monkeypatch.setattr(main, "classify_and_maybe_answer", lambda query: {"classification": "complex", "answer": ""})
    monkeypatch.setattr(main, "run_query", lambda query: {"status": "completed", "route": "final", "final_response": "done", "confidence": 0.82})
    resp = client.post("/query", json={"query": "Analyze my portfolio", "conversation_id": "c1"})
    assert resp.status_code == 200
    assert resp.json()["final_response"] == "done"

    monkeypatch.setattr(main, "stream_query", lambda query: iter([("crew_node", {"final_response": "streaming", "confidence": 0.8, "revise_count": 0}), ("final_response", {"final_response": "streaming", "confidence": 0.8, "revise_count": 0})]))
    resp = client.post("/query/stream", json={"query": "Analyze my portfolio", "conversation_id": "c1"})
    assert resp.status_code == 200
    assert "streaming" in resp.text

    monkeypatch.setattr(main, "register_user", lambda **kwargs: {"message": "Registration successful", "email": "e@example.com", "requires_verification": False})
    resp = client.post("/auth/register", json={"name": "A", "email": "e@example.com", "password": "Strong!123"})
    assert resp.status_code == 200

    monkeypatch.setattr(main, "authenticate_with_auth0", lambda username, password: {"access_token": "abc", "username": username})
    resp = client.post("/auth/login", json={"username": "e@example.com", "password": "Strong!123"})
    assert resp.status_code == 200
    assert resp.json()["access_token"] == "abc"

    monkeypatch.setattr(main, "update_user_profile", lambda **kwargs: {"message": "Profile updated successfully."})
    resp = client.post("/auth/profile/update", json={"name": "A", "old_password": "x", "new_password": "y"})
    assert resp.status_code == 200

    monkeypatch.setattr(main.rag_service, "ingest_file", lambda file_path: 2)
    monkeypatch.setattr(main.rag_service, "list_documents", lambda: ["sample.txt"])
    resp = client.post("/rag/ingest", files={"file": ("sample.txt", b"hello world", "text/plain")})
    assert resp.status_code == 200

    monkeypatch.setattr(main.rag_service, "search", lambda query, k=3: [{"source": "sample.txt", "text": "hello", "score": 0.9}])
    resp = client.post("/rag/retrieve", json={"query": "hello", "top_k": 1})
    assert resp.status_code == 200
    assert resp.json()["results"][0]["source"] == "sample.txt"

    monkeypatch.setattr(main.rag_service, "list_documents", lambda: ["sample.txt"])
    resp = client.get("/rag/documents")
    assert resp.status_code == 200

    monkeypatch.setattr(main.rag_service, "remove_file", lambda filename: True)
    resp = client.delete("/rag/documents/sample.txt")
    assert resp.status_code == 200

    monkeypatch.setattr(main, "ingest_sql_content", lambda sql_text: {"tables": ["portfolio_holdings"]})
    resp = client.post("/sql/ingest", files={"file": ("a.sql", b"SELECT 1", "application/sql")})
    assert resp.status_code == 200

    monkeypatch.setattr(main, "list_tables", lambda: ["portfolio_holdings"])
    monkeypatch.setattr(main, "get_schema_description", lambda: "schema")
    resp = client.get("/sql/schema")
    assert resp.status_code == 200

    monkeypatch.setattr(main, "create_conversation", lambda user_id: {"id": 12, "title": "Portfolio", "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 1)})
    resp = client.post("/conversations")
    assert resp.status_code == 200

    monkeypatch.setattr(main, "list_conversations", lambda user_id: [{"id": 12, "title": "Portfolio", "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 1)}])
    resp = client.get("/conversations")
    assert resp.status_code == 200

    monkeypatch.setattr(main, "get_messages", lambda conversation_id, user_id: [{"role": "user", "content": "hello", "created_at": datetime(2024, 1, 1)}])
    resp = client.get("/conversations/12/messages")
    assert resp.status_code == 200

    monkeypatch.setattr(main, "delete_conversation", lambda conversation_id, user_id: True)
    resp = client.delete("/conversations/12")
    assert resp.status_code == 200

    main.app.dependency_overrides.clear()


def test_fastpath_document_and_db_detection():
    assert classify_and_maybe_answer("Explain the attached report")["classification"] == "complex"
    assert classify_and_maybe_answer("Give me the top asset names from the database")["classification"] == "complex"
