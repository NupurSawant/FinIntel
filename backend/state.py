from typing import TypedDict


class GraphState(TypedDict, total=False):
    # input
    query: str

    # guardrail node
    is_safe: bool
    block_reason: str
    detected_intents: list[str]

    # crew node
    draft_answer: str

    # critic / reflection node
    confidence: float
    is_well_attributed: bool
    critic_issues: list[str]
    revision_instructions: str

    # routing / control
    revise_count: int
    route: str  # "final" | "revise" | "human_handoff" | "blocked"

    # output
    final_response: str
    status: str  # "completed" | "blocked" | "escalated"
