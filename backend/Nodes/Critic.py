import logging

from Agents.CriticAgent import run_critic_review
from llm import llm
from Observability.langfuse_client import observe_span
from state import GraphState

logger = logging.getLogger("finance_workflow")
logging.basicConfig(level=getattr(logging, llm.LOG_LEVEL, logging.INFO))


def critic_node(state: GraphState) -> GraphState:
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
