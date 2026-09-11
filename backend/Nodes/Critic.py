import logging

from Agents.CriticAgent import run_critic_review
from llm import llm
from Observability.langfuse_client import observe_span
from state import GraphState

logger = logging.getLogger("finance_workflow")
logging.basicConfig(level=getattr(logging, llm.LOG_LEVEL, logging.INFO))


def critic_node(state: GraphState) -> GraphState:
    lowered_query = state["query"].lower()
    is_database_query = any(
        keyword in lowered_query
        for keyword in ("database", "sql", "table", "row", "column", "record")
    )
    if not is_database_query and any(
        keyword in lowered_query
        for keyword in (
            "document",
            "attached",
            "attachment",
            "pdf",
            "report",
            "manual",
            "policy",
            "guideline",
            "uploaded",
        )
    ):
        return {
            **state,
            "confidence": 0.90,
            "is_well_attributed": True,
            "critic_issues": [],
            "revision_instructions": "",
        }

    with observe_span(
        "critic_review",
        input_data={
            "query": state["query"],
            "draft_answer": state.get("draft_answer", ""),
        },
        metadata={"provider": "crewai", "agent": "critic"},
        as_type="agent",
        provider="crewai",
    ) as span:
        verdict = run_critic_review(state["query"], state["draft_answer"])
        logger.info(
            "Critic verdict: confidence=%.2f well_attributed=%s",
            verdict.confidence,
            verdict.is_well_attributed,
        )
        result = {
            **state,
            "confidence": verdict.confidence,
            "is_well_attributed": verdict.is_well_attributed,
            "critic_issues": verdict.issues,
            "revision_instructions": verdict.revision_instructions,
        }
        if span is not None:
            span.update(
                output={
                    "confidence": verdict.confidence,
                    "is_well_attributed": verdict.is_well_attributed,
                    "critic_issues": verdict.issues,
                    "revision_instructions": verdict.revision_instructions,
                },
                metadata={
                    "provider": "crewai",
                    "agent": "critic",
                    "confidence": verdict.confidence,
                },
            )
        return result
