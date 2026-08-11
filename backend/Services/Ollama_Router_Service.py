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


def _mentions_uploaded_document(query: str) -> bool:
    lowered = query.lower()
    return any(kw in lowered for kw in _DOCUMENT_REFERENCE_KEYWORDS)


def _mentions_database_query(query: str) -> bool:
    lowered = query.lower()
    return any(kw in lowered for kw in _DATABASE_QUERY_KEYWORDS)


class RouterVerdict(BaseModel):
    classification: Literal["simple", "complex"] = Field(
        ...,
        description=(
            "'simple' for greetings, small talk, or generic definitional/educational "
            "questions answerable from general knowledge with no internal portfolio, "
            "document, or market data needed. 'complex' for anything referencing "
            "'our' portfolio/holdings, an uploaded document/report, specific tickers "
            "or live prices, risk exposure, benchmark comparisons, or multi-step "
            "financial reasoning."
        ),
    )
    answer: str = Field(
        "",
        description=(
            "If classification is 'simple', a direct 2-4 sentence plain-language "
            "answer. If classification is 'complex', leave this empty."
        ),
    )


_ROUTER_PROMPT = """Classify this message as SIMPLE or COMPLEX, and if SIMPLE, answer it.

SIMPLE examples: "hello", "hi", "thanks", "what is a mutual fund?", "explain diversification"
COMPLEX examples: "what are the top risk factors in our tech portfolio?", "summarize the report I uploaded", "how is AAPL doing today?"

Message: {query}"""


def _get_structured_llm():
    from langchain_ollama import ChatOllama

    llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
    return llm.with_structured_output(RouterVerdict)


def classify_and_maybe_answer(query: str) -> dict:
    """
    Returns {"classification": "simple"|"complex", "answer": str}.
    Always returns a dict - never raises - callers can safely fall back
    to the full crew pipeline on any failure.
    """
    if _mentions_uploaded_document(query):
        logger.info(
            "Ollama pre-router: query references an uploaded document - forcing COMPLEX without calling Ollama."
        )
        return {"classification": "complex", "answer": ""}

    if _mentions_database_query(query):
        logger.info(
            "Ollama pre-router: query references database content - forcing COMPLEX without calling Ollama."
        )
        return {"classification": "complex", "answer": ""}

    try:
        with observe_span(
            "ollama_router",
            input_data={"query": query},
            metadata={
                "provider": "ollama",
                "model": OLLAMA_MODEL,
                "route": "pre_router",
            },
            as_type="chain",
            provider="ollama",
            model=OLLAMA_MODEL,
        ) as span:
            structured_llm = _get_structured_llm()
            verdict: RouterVerdict = structured_llm.invoke(
                _ROUTER_PROMPT.format(query=query)
            )
            logger.info(
                "Ollama pre-router verdict: classification=%s answer=%r",
                verdict.classification,
                verdict.answer[:80],
            )

            classification = verdict.classification
            answer = (verdict.answer or "").strip()

            if classification == "simple" and not answer:
                logger.info(
                    "Ollama pre-router: classified simple but answer was empty - downgrading to complex."
                )
                classification = "complex"

            result = {"classification": classification, "answer": answer}
            if span is not None:
                span.update(
                    output=result,
                    metadata={
                        "provider": "ollama",
                        "model": OLLAMA_MODEL,
                        "route": "pre_router",
                        "classification": classification,
                    },
                )
            return result

    except Exception as e:
        logger.warning(
            "Ollama pre-router unavailable or failed (%s) - falling back to full crew pipeline.",
            e,
        )
        return {"classification": "complex", "answer": ""}
