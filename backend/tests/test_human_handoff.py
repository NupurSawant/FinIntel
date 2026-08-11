import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import glob

from Nodes.HumanHandoff import human_handoff_node
from Nodes.route import decide_route
from Services.Email_Service import ESCALATIONS_DIR


def test_decide_route_human_handoff():
    # 1. High confidence -> final
    state1 = {"confidence": 0.85, "revise_count": 0}
    assert decide_route(state1) == "final"

    # 2. Low confidence but retries < 3 -> revise
    state2 = {"confidence": 0.50, "revise_count": 1}
    assert decide_route(state2) == "revise"

    # 3. Low confidence AND retries >= 3 -> human_handoff
    state3 = {"confidence": 0.50, "revise_count": 3}
    assert decide_route(state3) == "human_handoff"


def test_human_handoff_node_execution():
    test_state = {
        "query": "Should I allocate 100% of my portfolio into risky cryptocurrency?",
        "confidence": 0.40,
        "revise_count": 3,
        "issues": ["Low attribution confidence", "High financial risk advice"],
        "draft_answer": "Cryptocurrency is highly volatile.",
    }

    res_state = human_handoff_node(test_state)

    assert res_state["status"] == "escalated"
    assert res_state["route"] == "final"
    assert "⚠️ **Query Escalated for Human Review**" in res_state["final_response"]

    # Verify log file generated in escalations directory
    escalation_files = glob.glob(os.path.join(ESCALATIONS_DIR, "escalation_*.json"))
    assert len(escalation_files) > 0
