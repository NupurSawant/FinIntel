from langgraph.graph import END, StateGraph

from Nodes.Crew import crew_node
from Nodes.Critic import critic_node
from Nodes.HumanHandoff import human_handoff_node
from Nodes.route import route_decision_node
from Observability.langfuse_client import observe_span
from state import GraphState


def final_response_node(state: GraphState) -> GraphState:
    if state.get("status") in ("blocked", "escalated"):
        return state
    return {
        **state,
        "final_response": state.get("draft_answer", ""),
        "status": "completed",
    }


def route_branch(state: GraphState) -> str:
    route = state.get("route", "final")
    if route == "revise":
        return "revise"
    if route == "human_handoff":
        return "human_handoff"
    return "final"


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("crew_node", crew_node)
    graph.add_node("critic_node", critic_node)
    graph.add_node("route_decision", route_decision_node)
    graph.add_node("human_handoff", human_handoff_node)
    graph.add_node("final_response", final_response_node)

    graph.set_entry_point("crew_node")

    graph.add_edge("crew_node", "critic_node")
    graph.add_edge("critic_node", "route_decision")

    graph.add_conditional_edges(
        "route_decision",
        route_branch,
        {
            "final": "final_response",
            "revise": "crew_node",
            "human_handoff": "human_handoff",
        },
    )

    graph.add_edge("human_handoff", "final_response")
    graph.add_edge("final_response", END)

    return graph.compile()


_compiled_graph = None


def get_compiled_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


def stream_query(query: str):
    """
    Streams graph execution node-by-node in real time. Yields
    (node_name, partial_state) as each node actually finishes running,
    so the timing genuinely reflects backend work (LLM calls take real
    seconds), not a simulated animation.
    """
    with observe_span(
        "graph_stream",
        input_data={"query": query},
        metadata={"provider": "langgraph", "workflow": "finance_graph"},
        as_type="chain",
        provider="langgraph",
    ) as span:
        graph = get_compiled_graph()
        initial_state: GraphState = {"query": query, "revise_count": 0}
        for step in graph.stream(initial_state):
            for node_name, node_state in step.items():
                yield node_name, {
                    "confidence": node_state.get("confidence"),
                    "revise_count": node_state.get("revise_count", 0),
                    "route": node_state.get("route"),
                    "final_response": node_state.get("final_response")
                    or node_state.get("draft_answer"),
                    "status": node_state.get("status"),
                }
        if span is not None:
            span.update(output={"query": query, "status": "streamed"})


def run_query(query: str) -> GraphState:
    with observe_span(
        "graph_execution",
        input_data={"query": query},
        metadata={"provider": "langgraph", "workflow": "finance_graph"},
        as_type="chain",
        provider="langgraph",
    ) as span:
        graph = get_compiled_graph()
        initial_state: GraphState = {"query": query, "revise_count": 0}
        final_state = graph.invoke(initial_state)
        if span is not None:
            span.update(
                output=final_state,
                metadata={
                    "provider": "langgraph",
                    "workflow": "finance_graph",
                    "status": final_state.get("status"),
                },
            )
        return final_state
