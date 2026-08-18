import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import glob

from Agents.CriticAgent import detect_incomplete_legal_question
from Nodes.HumanHandoff import human_handoff_node
from Nodes.route import decide_route
from Services.Email_Service import ESCALATIONS_DIR


def test_human_handoff_reports_local_log_when_smtp_not_configured(monkeypatch):
    monkeypatch.delenv("SMTP_SERVER", raising=False)
    monkeypatch.delenv("SMTP_USERNAME", raising=False)
    monkeypatch.delenv("SMTP_PASSWORD", raising=False)
    monkeypatch.delenv("SMTP_APP_PASSWORD", raising=False)

    state = {
        "query": "Can a bank seize collateral without contract terms or governing law?",
        "confidence": 0.35,
        "revise_count": 3,
        "issues": ["Missing governing law", "Missing jurisdiction"],
        "draft_answer": "Legal answer requires contract review.",
    }

    result = human_handoff_node(state)

    assert result["status"] == "escalated"
    assert "logged locally" in result["final_response"].lower()
    assert "no email was sent" in result["final_response"].lower()


def test_incomplete_legal_fact_pattern_is_flagged_for_human_review():
    query = (
        "Using only this fact pattern—'Counterparty X failed to post USD 180M of collateral "
        "after a mark-to-market loss, and the bank is now deciding whether to terminate "
        "the derivative portfolio under ISDA, Basel III, and local insolvency law'—"
        "determine the exact legal status, exposure calculation, and remediation required "
        "without any contract terms, governing law, or jurisdiction details."
    )

    flagged, issues, instruction = detect_incomplete_legal_question(query, "")

    assert flagged is True
    assert "contract terms" in " ".join(issues).lower()
    assert "governing law" in instruction.lower()


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
