"""
Lightweight pre-routing using a local Ollama model.

Classifies incoming queries as SIMPLE (greetings, small talk, generic
definitional questions - e.g. "what is a mutual fund?") or COMPLEX (anything
requiring internal portfolio data, uploaded documents, live market data, or
multi-step financial/risk analysis).

SIMPLE queries are answered directly by Ollama, bypassing the CrewAI
Manager -> specialist -> Critic pipeline entirely. COMPLEX queries fall
through to the existing graph unchanged.

Deterministic override: any explicit reference to an uploaded document
("document", "attached", "uploaded", "pdf", etc.) always forces COMPLEX
without even calling Ollama. Small local models are unreliable at weighing
this signal correctly - e.g. "From Attached Document - Explain me Credit
Risk Classification" reads surface-similar to a generic definitional
question ("explain diversification"), and a 3B model can misclassify it
as SIMPLE, answering from general knowledge instead of routing to the RAG
Agent. This is the same principle as the guardrail check elsewhere in this
project: use a fast, deterministic rule for an unambiguous signal instead
of trusting LLM judgment.

Uses ChatOllama.with_structured_output() (JSON-schema constrained decoding)
for the remaining ambiguous cases, since small local models are unreliable
at freely producing valid JSON in their own text.

Fail-safe: if Ollama is unreachable, times out, isn't installed, or the
call raises for any reason, this defaults to COMPLEX so every query still
gets a real answer via the full pipeline rather than silently failing.
"""

import logging
import os
from typing import Literal

from pydantic import BaseModel, Field

from Observability.langfuse_client import observe_span

logger = logging.getLogger("finance_workflow")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

_DOCUMENT_REFERENCE_KEYWORDS = [
    "document",
    "attached",
    "attachment",
    "pdf",
    "report",
    "manual",
    "policy",
    "guideline",
]

_DATABASE_QUERY_KEYWORDS = [
    "database",
    "sql",
    "table",
    "row",
    "column",
    "record",
    "asset_risk_logs",
    "portfolio_holdings",
    "investment_decisions",
    "market_indicators",
    "portfolios",
    "risk logs",
    "risk log",
    "risk score",
    "risk scores",
    "asset names",
    "from the database",
    "from database",
    "query",
]


_ACTIONABLE_RECOMMENDATION_KEYWORDS = [
    "top",
    "best",
    "recommend",
    "recommendation",
    "recommendations",
    "advice",
    "advise",
    "suggest",
    "suggestion",
    "give me",
    "which",
    "where should i",
    "how to invest",
    "how should i",
    "performer",
    "performers",
    "compare",
    "comparison",
    "analysis",
    "historical",
    "log",
    "logs",
    "holding",
    "holdings",
    "portfolio",
    "portfolios",
    "database",
    "document",
    "report",
    "pdf",
    "my",
    "our",
    "asset_risk_logs",
    "portfolio_holdings",
    "investment_decisions",
    "market_indicators",
]

_GREETING_WORDS = {
    "hi",
    "hello",
    "hey",
    "greetings",
    "good morning",
    "good afternoon",
    "good evening",
    "namaste",
    "thanks",
    "thank you",
    "bye",
    "goodbye",
}


def _mentions_uploaded_document(query: str) -> bool:
    lowered = query.lower()
    return any(kw in lowered for kw in _DOCUMENT_REFERENCE_KEYWORDS)


def _mentions_database_query(query: str) -> bool:
    lowered = query.lower()
    return any(kw in lowered for kw in _DATABASE_QUERY_KEYWORDS)


def _is_actionable_query(query: str) -> bool:
    lowered = query.lower().strip()
    return any(kw in lowered for kw in _ACTIONABLE_RECOMMENDATION_KEYWORDS)


def _is_simple_greeting(query: str) -> bool:
    cleaned = query.strip().lower().rstrip("!.,?")
    return cleaned in _GREETING_WORDS


class RouterVerdict(BaseModel):
    classification: Literal["simple", "complex"] = Field(
        ...,
        description=(
            "'simple' for greetings, small talk, or general educational/definitional "
            "questions (e.g. 'what is a mutual fund?'). 'complex' for any actionable investment "
            "recommendations, top performers, stock queries, portfolio analysis, or multi-step reasoning."
        ),
    )
    answer: str = Field(
        "",
        description=(
            "If classification is 'simple', a clear, helpful 2-4 sentence plain-language "
            "explanation or friendly response. If classification is 'complex', leave this completely empty."
        ),
    )


USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() in ("true", "1", "yes")

_ROUTER_PROMPT = """Classify this message as SIMPLE or COMPLEX, and if SIMPLE, provide a clear answer:

SIMPLE examples: "hello", "hi", "thanks", "what is a mutual fund?", "explain diversification", "what is SIP?"
COMPLEX examples: "give me top performers in SIPs", "how to invest 10000 per month", "summarize tech sector market risks", "how is AAPL doing today?"

Message: {query}"""


def _get_structured_llm():
    """
    Returns structured LLM for pre-routing.
    Uses ChatOllama on localhost if enabled and available.
    Falls back to Azure OpenAI (llm.get_langchain_llm()) in deployed/cloud environments.
    """
    if USE_OLLAMA:
        try:
            from langchain_ollama import ChatOllama

            local_llm = ChatOllama(
                model=OLLAMA_MODEL,
                base_url=OLLAMA_BASE_URL,
                temperature=0,
                timeout=2.0,
            )
            return local_llm.with_structured_output(RouterVerdict), "ollama"
        except Exception as e:
            logger.info(
                "Local Ollama not available (%s), falling back to Azure OpenAI for pre-router.",
                e,
            )

    from llm import llm

    azure_llm = llm.get_langchain_llm()
    return azure_llm.with_structured_output(RouterVerdict), "azure_openai"


def classify_and_maybe_answer(query: str) -> dict:
    """
    Returns {"classification": "simple"|"complex", "answer": str}.
    Always returns a dict - never raises - callers can safely fall back
    to the full crew pipeline on any failure.
    """
    if _is_simple_greeting(query):
        logger.info("Pre-router: simple greeting detected.")
        return {
            "classification": "simple",
            "answer": "Hello! I am your AI Financial Assistant. How can I help you with your investment portfolio, market analysis, or risk evaluation today?",
        }

    if _mentions_uploaded_document(query):
        logger.info(
            "Pre-router: query references an uploaded document - forcing COMPLEX."
        )
        return {"classification": "complex", "answer": ""}

    if _mentions_database_query(query):
        logger.info(
            "Pre-router: query references database content - forcing COMPLEX."
        )
        return {"classification": "complex", "answer": ""}

    if _is_actionable_query(query):
        logger.info(
            "Pre-router: query contains actionable recommendation/portfolio request - forcing COMPLEX."
        )
        return {"classification": "complex", "answer": ""}

    try:
        structured_llm, provider = _get_structured_llm()
        with observe_span(
            "pre_router",
            input_data={"query": query},
            metadata={
                "provider": provider,
                "model": OLLAMA_MODEL if provider == "ollama" else "azure_openai",
                "route": "pre_router",
            },
            as_type="chain",
            provider=provider,
        ) as span:
            verdict: RouterVerdict = structured_llm.invoke(
                _ROUTER_PROMPT.format(query=query)
            )
            logger.info(
                "Pre-router verdict (%s): classification=%s answer=%r",
                provider,
                verdict.classification,
                (verdict.answer or "")[:80],
            )

            classification = verdict.classification
            answer = (verdict.answer or "").strip()

            if classification == "simple":
                if not answer or answer.upper() in ("TRUE", "FALSE", "SIMPLE", "COMPLEX") or len(answer) < 5:
                    answer = "Hello! I am your AI Financial Assistant. How can I help you with your investment portfolio, market analysis, or risk evaluation today?"

            result = {"classification": classification, "answer": answer}
            if span is not None:
                span.update(
                    output=result,
                    metadata={
                        "provider": provider,
                        "route": "pre_router",
                        "classification": classification,
                    },
                )
            return result

    except Exception as e:
        logger.warning(
            "Pre-router execution failed (%s) - falling back to full crew pipeline.",
            e,
        )
        return {"classification": "complex", "answer": ""}
