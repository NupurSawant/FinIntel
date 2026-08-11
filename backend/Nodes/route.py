from llm import llm
from Observability.langfuse_client import observe_span
from state import GraphState


def decide_route(state: GraphState) -> str:
    confidence = state.get("confidence", 0.0)
    revise_count = state.get("revise_count", 0)

    if confidence >= llm.CONFIDENCE_THRESHOLD:
        return "final"

    max_retries = getattr(llm, "MAX_REVISE_RETRIES", 3)
    if revise_count >= max_retries:
        return "human_handoff"

    return "revise"


def route_decision_node(state: GraphState) -> GraphState:
    """
    Evaluates current state confidence & revise_count to decide whether to loop
    back to crew_node or proceed to final_response.
    """
    with observe_span(
        "route_decision",
        input_data={"state": state},
        metadata={"provider": "workflow", "agent": "router"},
        as_type="span",
        provider="workflow",
    ) as span:
        route = decide_route(state)
        updated_revise_count = state.get("revise_count", 0)
        if route == "revise":
            updated_revise_count += 1
        result = {**state, "route": route, "revise_count": updated_revise_count}
        if span is not None:
            span.update(
                output={"route": route, "revise_count": updated_revise_count},
                metadata={"provider": "workflow", "agent": "router", "route": route},
            )
        return result
