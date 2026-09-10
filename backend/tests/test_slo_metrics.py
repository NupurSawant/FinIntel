import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Services.SLO_Metrics_Service import (
    get_aggregated_slo_metrics,
    record_guardrail_block,
    record_query_metric,
)


def test_slo_metrics_record_and_aggregate():
    record_guardrail_block()
    record_query_metric(
        query="What are major global market risk drivers?",
        latency_sec=1.85,
        router_sec=0.32,
        confidence=0.88,
        revisions=0,
        status="completed",
        route="crew",
        tokens=1100,
        agent_latencies={"Manager": 0.3, "Risk": 0.9, "Critic": 0.4},
    )

    metrics = get_aggregated_slo_metrics()

    assert "end_to_end_response_time" in metrics
    assert "router_time" in metrics
    assert "individual_agent_latency text" not in metrics
    assert "individual_agent_latency" in metrics
    assert "critic_revision_rate" in metrics
    assert "confidence_score_distribution" in metrics
    assert "routing_accuracy" in metrics
    assert "rag_retrieval_success" in metrics
    assert "sql_success_rate" in metrics
    assert "market_api_success" in metrics
    assert "guardrail_blocks" in metrics
    assert "human_handoff_rate" in metrics
    assert "error_rate" in metrics
    assert "cost_savings" in metrics
    assert "average_tokens" in metrics

    assert metrics["guardrail_blocks"] >= 1
    assert metrics["end_to_end_response_time"] > 0
    assert metrics["confidence_score_distribution"] > 0
