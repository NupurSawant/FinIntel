import json
import re

from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel, Field

from llm import llm


def detect_incomplete_legal_question(query: str, draft_answer: str) -> tuple[bool, list[str], str]:
    """Only strict-check legal queries that explicitly lack the governing legal facts needed for a definitive answer."""
    text = (query or "") + " " + (draft_answer or "")
    lowered = text.lower()

    # Narrow strict mode to a small set of patterns that are truly not answerable
    # without the governing legal facts. Normal finance/legal questions remain allowed.
    strict_missing_fact_patterns = [
        "contract terms, governing law, and insolvency regime are all unknown",
        "contract terms, governing law, and insolvency regime are unknown",
        "when the contract terms, governing law, and insolvency regime are all unknown",
        "without any contract terms, governing law, or jurisdiction details",
        "without any contract terms, governing law, or jurisdiction",
        "without contract terms, governing law, or jurisdiction details",
        "without the contract terms, governing law, or jurisdiction",
        "governing law and jurisdiction are missing",
        "without governing law and jurisdiction",
        "no governing law and no jurisdiction",
        "contract terms and governing law are unknown",
        "governing law, and jurisdiction are all unknown",
    ]

    explicit_missing_facts = any(pattern in lowered for pattern in strict_missing_fact_patterns)
    if not explicit_missing_facts:
        # Also allow the older, narrower form where the request clearly says the key facts are missing
        missing_legal_facts = [
            "without any contract terms",
            "without contract terms",
            "without any governing law",
            "without governing law",
            "without any jurisdiction",
            "without jurisdiction",
            "no contract terms",
            "no governing law",
            "no jurisdiction details",
            "without any jurisdiction details",
            "without jurisdiction details",
            "without the relevant governing law",
            "without the governing law",
        ]
        if not any(phrase in lowered for phrase in missing_legal_facts):
            return False, [], ""

    legal_issues = [
        "close-out netting",
        "netting",
        "seize collateral",
        "terminate the derivative portfolio",
        "derivative counterparty defaults",
        "defaulting counterparty",
        "legal status",
        "legal exposure",
        "regulatory capital impact",
        "remediation required",
        "determine the exact legal status",
        "determine legal status",
        "exact legal status",
        "exposure calculation",
        "close-out rights",
        "insolvency law",
        "isda",
        "basel",
        "governing law",
        "jurisdiction",
        "contract terms",
    ]
    if not any(keyword in lowered for keyword in legal_issues):
        return False, [], ""

    # Required: the question has to be asking for a legal conclusion or immediate remedy.
    definitive_legal_request = any(
        phrase in lowered
        for phrase in [
            "can you confirm whether",
            "determine the exact legal status",
            "determine legal status",
            "exact legal status",
            "legal exposure",
            "remediation required",
            "close-out rights",
            "immediately exercise",
            "seize collateral",
            "exercise close-out netting",
            "recover usd",
            "legal answer",
            "can immediately",
            "without the actual csa",
            "without the contract terms",
        ]
    )
    if not definitive_legal_request:
        return False, [], ""

    issues = [
        "The question explicitly lacks the contract terms, governing law, and/or jurisdiction needed for a reliable legal answer.",
        "The fact pattern is incomplete for a definitive legal status, exposure calculation, or remediation decision.",
        "Any answer providing legal status, exposure, or remediation would be speculative and should be escalated.",
    ]
    instruction = (
        "Do not provide a definitive legal conclusion. Request the governing law, jurisdiction, contract terms, "
        "ISDA terms, and insolvency framework before assessing legal status, exposure, or remediation. "
        "Route to human review because the legal answer is not determinable from the current fact pattern alone."
    )
    return True, issues, instruction


class CriticVerdict(BaseModel):
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence the draft answer is accurate and well-supported.",
    )
    is_well_attributed: bool = Field(
        ..., description="Whether every material claim cites a source/tool result."
    )
    issues: list[str] = Field(
        default_factory=list, description="Specific problems found, if any."
    )
    revision_instructions: str = Field(
        "", description="Concrete instructions for revision, if confidence is low."
    )


def CriticAgent(llm_config=llm) -> Agent:
    agent_llm = llm_config.get_llm()

    critic_agent = Agent(
        role="Financial Insight Critic / Quality Reviewer",
        goal=(
            "Evaluate whether the response is accurate, well supported,internally consistent, and sufficient to answer the user's question."
            "Only recommend revision if important factual information is missing or incorrect."
        ),
        backstory=(
            "You are an experienced financial QA reviewer. "
            "Your job is to determine whether the answer is accurate enough to deliver to the end user."
            "Minor wording improvements should not reduce confidence. "
            "Only major factual errors, missing evidence, or contradictions should significantly reduce confidence."
        ),
        llm=agent_llm,
        allow_delegation=False,
        verbose=True,
    )

    return critic_agent


def run_critic_review(query: str, draft_answer: str) -> CriticVerdict:
    critic = CriticAgent()

    task = Task(
        description=(
            f"Original analyst query:\n{query}\n\n"
            f"Draft answer produced by the specialist team:\n{draft_answer}\n\n"
            "You are the final quality reviewer for an AI-powered financial analysis system.\n\n"
            "Your responsibility is to determine whether the draft answer is accurate enough "
            "to be delivered to the user. Focus on factual correctness, internal consistency, "
            "completeness, and whether the answer addresses the user's question.\n\n"
            "Evaluate using the following confidence rubric:\n"
            "- 0.90-1.00 : The answer is complete, accurate, internally consistent, "
            "well-supported, and ready to deliver.\n"
            "- 0.80-0.89 : The answer is accurate and complete. Minor wording, formatting, "
            "or presentation improvements are possible but revision is NOT required.\n"
            "- 0.70-0.79 : The answer is generally correct with minor missing details. "
            "It is still acceptable unless important information is missing.\n"
            "- Below 0.70 : The answer contains factual errors, unsupported claims, "
            "contradictions, or does not adequately answer the user's question.\n\n"
            "IMPORTANT RULES:\n"
            "1. Do NOT reduce confidence for minor wording, grammar, formatting, or writing style.\n"
            "2. Do NOT invent missing issues just because the answer could be improved.\n"
            "3. Only recommend revision when there are important factual, logical, or evidence-related problems.\n"
            "4. If the answer correctly addresses the user's question and contains no major issues, "
            "confidence should normally be 0.80 or higher.\n"
            "5. If there are only minor suggestions, keep confidence above 0.75 and leave "
            "revision_instructions empty.\n\n"
            "Return ONLY a valid JSON object with these keys:\n"
            "- confidence (float between 0 and 1)\n"
            "- is_well_attributed (boolean)\n"
            "- issues (list of strings)\n"
            "- revision_instructions (string; leave empty if no major revision is needed)\n\n"
            "Do not return any explanation outside the JSON object."
        ),
        expected_output="A single JSON object matching the CriticVerdict schema.",
        agent=critic,
    )

    crew = Crew(
        agents=[critic], tasks=[task], process=Process.sequential, verbose=False
    )
    result = crew.kickoff()

    raw = str(result).strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
    try:
        data = json.loads(raw)
        flagged, missing_issues, missing_instruction = detect_incomplete_legal_question(
            query, draft_answer
        )
        if flagged:
            data["confidence"] = min(float(data.get("confidence", 0.0)), 0.45)
            data["is_well_attributed"] = False
            data["issues"] = list(
                dict.fromkeys([*(data.get("issues", [])), *missing_issues])
            )
            data["revision_instructions"] = (
                missing_instruction
                if not str(data.get("revision_instructions", "")).strip()
                else data["revision_instructions"] + " " + missing_instruction
            )
        return CriticVerdict(**data)
    except (json.JSONDecodeError, TypeError, ValueError):
        flagged, missing_issues, missing_instruction = detect_incomplete_legal_question(
            query, draft_answer
        )
        if flagged:
            return CriticVerdict(
                confidence=0.45,
                is_well_attributed=False,
                issues=missing_issues,
                revision_instructions=missing_instruction,
            )
        return CriticVerdict(
            confidence=0.0,
            is_well_attributed=False,
            issues=["Critic output could not be parsed into structured verdict."],
            revision_instructions="Re-run synthesis ensuring output is well-attributed.",
        )
