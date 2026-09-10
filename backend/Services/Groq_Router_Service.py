"""Groq-backed intent pre-router used by both query endpoints."""

import logging
from typing import Literal

from pydantic import BaseModel, Field

from Observability.langfuse_client import observe_span
from llm import llm

logger = logging.getLogger("finance_workflow")

_DOCUMENT_REFERENCE_KEYWORDS = (
    "document", "attached", "attachment", "pdf", "report", "manual", "policy", "guideline"
)
_DATABASE_QUERY_KEYWORDS = (
    "database", "sql", "table", "row", "column", "record", "asset_risk_logs",
    "portfolio_holdings", "investment_decisions", "market_indicators", "portfolio",
)
_ACTIONABLE_KEYWORDS = (
    "top", "best", "recommend", "advice", "suggest", "give me", "which",
    "how to invest", "performer", "compare", "analysis", "historical", "holding",
)
_GREETING_WORDS = {
    "hi", "hello", "hey", "greetings", "good morning", "good afternoon",
    "good evening", "namaste", "thanks", "thank you", "bye", "goodbye",
}


class RouterVerdict(BaseModel):
    classification: Literal["simple", "complex"] = Field(...)
    answer: str = Field("")


def _is_simple_greeting(query: str) -> bool:
    return query.strip().lower().rstrip("!.,?") in _GREETING_WORDS


def _mentions_uploaded_document(query: str) -> bool:
    return any(k in query.lower() for k in _DOCUMENT_REFERENCE_KEYWORDS)


def _mentions_database_query(query: str) -> bool:
    return any(k in query.lower() for k in _DATABASE_QUERY_KEYWORDS)


def _forced_complex(query: str) -> bool:
    lowered = query.lower()
    return (
        _mentions_uploaded_document(query)
        or _mentions_database_query(query)
        or any(k in lowered for k in _ACTIONABLE_KEYWORDS)
    )


def _get_structured_llm():
    return llm.get_langchain_llm().with_structured_output(RouterVerdict), "groq"


def classify_and_maybe_answer(query: str) -> dict:
    if _is_simple_greeting(query):
        return {
            "classification": "simple",
            "answer": "Hello! I am your AI Financial Assistant. How can I help you with your investment portfolio, market analysis, or risk evaluation today?",
        }
    if _forced_complex(query):
        return {"classification": "complex", "answer": ""}

    try:
        structured_llm, provider = _get_structured_llm()
        with observe_span(
            "pre_router",
            input_data={"query": query},
            metadata={"provider": provider, "model": llm.groq_model, "route": "pre_router"},
            as_type="chain",
            provider=provider,
        ) as span:
            verdict: RouterVerdict = structured_llm.invoke(
                "Classify as simple for greetings, small talk, or general educational "
                "questions; classify as complex for actionable financial analysis. "
                f"Message: {query}"
            )
            answer = (verdict.answer or "").strip()
            if verdict.classification == "simple" and len(answer) < 5:
                answer = "I can help explain financial concepts and analyze your portfolio."
            result = {"classification": verdict.classification, "answer": answer}
            if span is not None:
                span.update(output=result, metadata={"provider": provider, "classification": verdict.classification})
            return result
    except Exception as exc:
        logger.warning("Groq pre-router failed; using the full workflow: %s", exc)
        return {"classification": "complex", "answer": ""}
