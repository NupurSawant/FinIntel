"""
Human Handoff Node - Triggers escalation email dispatch to sawant.nupur25@gmail.com
when confidence score remains below threshold after maximum revision attempts.
"""

from Observability.langfuse_client import observe_span
from Services.Email_Service import DEFAULT_RECIPIENT, send_escalation_email
from state import GraphState


def human_handoff_node(state: GraphState) -> GraphState:
    """
    Handles escalation when max revision attempts fail to achieve confidence >= threshold.
    Dispatches escalation email to sawant.nupur25@gmail.com and returns an updated state.
    """
    with observe_span(
        "human_handoff",
        input_data={"state": state},
        metadata={"provider": "workflow", "agent": "human_handoff"},
        as_type="span",
        provider="workflow",
    ) as span:
        query = state.get("query", "")
        confidence = state.get("confidence", 0.0)
        issues = state.get("issues", [])
        revise_count = state.get("revise_count", 0)
        draft_answer = state.get("draft_answer", "")

        # 1. Trigger Email Service
        email_res = send_escalation_email(
            query=query,
            confidence=confidence,
            issues=issues,
            revise_count=revise_count,
            draft_answer=draft_answer,
            recipient_email=DEFAULT_RECIPIENT,
        )

        # 2. Construct user notification response
        escalation_notice = (
            f"⚠️ **Query Escalated for Human Review**\n\n"
            f"Your query required specialized financial review as the confidence score ({confidence:.2f}) "
            f"did not reach the required threshold after {revise_count} revision attempts.\n\n"
            f"An escalation alert email has been dispatched to `{DEFAULT_RECIPIENT}` containing the "
            f"query details, flagged critic issues, and agent analysis for manual financial review.\n\n"
            f"**Draft Specialist Analysis:**\n"
            f"{draft_answer}"
        )

        result: GraphState = {
            **state,
            "status": "escalated",
            "route": "final",
            "final_response": escalation_notice,
        }

        if span is not None:
            span.update(output={"status": "escalated", "recipient": DEFAULT_RECIPIENT})

        return result
