"""
Guardrail Service - Comprehensive Input Validation & Safety Engine.

Enforces strict compliance across 8 distinct guardrail rules:
1. Maximum Prompt Length (<= 5000 words)
2. Out-of-Domain & Jailbreak Defense (Off-topic queries, AI role impersonation, safety overrides)
3. Profanity & Respectful Language Filter
4. SQL Injection & Malicious Pattern Prevention
5. Personally Identifiable Information (PII) Protection
6. Unsafe / Guaranteed Financial Advice Restriction
7. Illegal Financial Activity & Fraud Detection
8. Resource Availability Check (Documents & SQL Database existence)
"""

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger("finance_workflow")


@dataclass
class GuardrailResult:
    is_blocked: bool
    reply: str
    category: str | None = None


# ---- REGEX & KEYWORD PATTERNS ----

# Rule 2: Jailbreak & Out-of-Domain patterns
JAILBREAK_PATTERNS = [
    r"\bpretend\s+you\s+are\s+not\s+an\s+ai\b",
    r"\bbypass\s+(your\s+)?safety\b",
    r"\bignore\s+your\s+instructions\b",
    r"\bignore\s+the\s+instructions\b",
    r"\bignore\s+(all\s+)?(previous\s+)?instructions\b",
    r"\bdisregard\s+(your\s+)?(instructions|safety)\b",
    r"\boverride\s+safety\b",
    r"\bact\s+as\s+dan\b",
    r"\bforget\s+your\s+rules\b",
    r"\bforget\s+all\s+instructions\b",
]

OUT_OF_DOMAIN_PATTERNS = [
    r"\b(recipe|recipes|bake|baking|cook|cooking|cake|chocolate|ingredient|ingredients|dish|food|dinner|lunch|breakfast|kitchen|soup|salad|pizza|burger)\b",
    r"\bwrite\s+(me\s+)?a\s+(love\s+)?poem\b",
    r"\b(poem|poetry|song|sing|singer|story|novel|fiction|fairytale)\b",
    r"\btell\s+me\s+a\s+joke\b",
    r"\b(joke|funny|humor|riddle)\b",
    r"\bwho\s+won\s+(the\s+)?ipl\b",
    r"\b(ipl|cricket|football|soccer|nba|world\s+cup|trophy|match|stadium|sports)\b",
    r"\bcreate\s+a\s+recipe\b",
    r"\bhow\s+to\s+cook\b",
    r"\bwho\s+is\s+(the\s+)?best\s+(actor|actress|singer|cricketer|footballer)\b",
    r"\b(movie|film|cinema|actor|actress|hollywood|bollywood)\b",
    r"\bwrite\s+a\s+story\b",
    r"\bmovie\s+review\b",
    r"\b(weather|temperature|rain|forecast)\b",
]

# Rule 3: Profanity & Insults
OFFENSIVE_PATTERNS = [
    r"\bidiot\b",
    r"\bstupid\b",
    r"\bdumb\b",
    r"\bfool\b",
    r"\bbastard\b",
    r"\bshit\b",
    r"\bfuck\b",
    r"\basshole\b",
    r"\bbitch\b",
]

# Rule 4: SQL Injection patterns
SQL_INJECTION_PATTERNS = [
    r"\bdrop\s+table\b",
    r"\bdelete\s+from\b",
    r"\binsert\s+into\b",
    r"\bupdate\s+\w+\s+set\b",
    r"\bunion\s+(all\s+)?select\b",
    r"\bdrop\s+database\b",
    r"\btruncate\s+table\b",
    r"\b1\s*=\s*1\b",
    r"\bor\s+1\s*=\s*1\b",
    r";\s*--",
    r"/\*.*?\*/",
]

# Rule 5: PII patterns
PII_CREDIT_CARD_PATTERN = r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"
PII_CVV_PATTERN = r"\b(cvv\d?|card\s+verification\s+value)\s*[:=]?\s*\d{3,4}\b"
PII_AADHAAR_PATTERN = r"\b[2-9]{1}[0-9]{3}\s?[0-9]{4}\s?[0-9]{4}\b"
PII_PAN_PATTERN = r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b"
PII_PASSPORT_PATTERN = r"\b[A-PR-WYa-pr-wy][1-9]\ds?\d{4}[1-9]\b"

PII_KEYWORDS = [
    r"\bcredit\s*card\b",
    r"\bcvv\b",
    r"\bpassword\b",
    r"\botp\b",
    r"\bbank\s*pin\b",
    r"\batm\s*pin\b",
    r"\baadhaar\b",
    r"\bpan\s*number\b",
    r"\bpassport\s*number\b",
]

# Rule 6: Sensitive / Unsafe Financial Advice
UNSAFE_ADVICE_PATTERNS = [
    r"\binvest\s+(my\s+)?life\s+savings\b",
    r"\bguarantee\s+profit\b",
    r"\bguaranteed\s+returns?\b",
    r"\btell\s+me\s+tomorrow'?s\s+stock\s+price\b",
    r"\bwhich\s+stock\s+will\s+double\b",
    r"\bguaranteed\s+investment\b",
]

# Rule 7: Illegal Financial Activity
ILLEGAL_FINANCE_PATTERNS = [
    r"\bmoney\s+laundering\b",
    r"\btax\s+fraud\b",
    r"\bevade\s+taxes\b",
    r"\binsider\s+trading\b",
    r"\binsider\s+information\b",
    r"\btrade\s+insider\s+information\b",
    r"\bmarket\s+manipulation\b",
    r"\bbypass\s+kyc\b",
    r"\bfake\s+invoice\b",
    r"\bponzi\s+scheme\b",
]

# Rule 8: Resource intent keywords
RESOURCE_DOC_PATTERNS = [
    r"\bdocument\b",
    r"\buploaded\s+doc\b",
    r"\bpdf\b",
    r"\bfile\b",
    r"\battachment\b",
]
RESOURCE_SQL_PATTERNS = [r"\bdatabase\b", r"\bsql\b", r"\btable\b", r"\bdb\b"]


def check_guardrails(
    query: str,
    has_documents: bool = True,
    has_tables: bool = True,
) -> GuardrailResult:
    """Inspects an incoming query against 8 Guardrail rules.
    Returns GuardrailResult(is_blocked=False) if clean, or GuardrailResult(is_blocked=True, reply=...) if blocked.
    """
    clean_query = query.strip()
    lower_query = clean_query.lower()

    # Rule 1: Length Limit (> 5,000 words or > 25,000 characters)
    word_count = len(clean_query.split())
    if word_count > 5000 or len(clean_query) > 25000:
        logger.info(
            "Guardrail blocked: Query exceeds maximum word count (%d words)", word_count
        )
        return GuardrailResult(
            is_blocked=True,
            reply="The query exceeds the maximum allowed length.",
            category="length_exceeded",
        )

    # Rule 2: Jailbreak & Out-of-Domain Questions
    for pattern in JAILBREAK_PATTERNS + OUT_OF_DOMAIN_PATTERNS:
        if re.search(pattern, lower_query):
            logger.info(
                "Guardrail blocked: Jailbreak/Out of domain query detected (%s)",
                pattern,
            )
            return GuardrailResult(
                is_blocked=True,
                reply="This application only answers finance and investment related questions.",
                category="out_of_domain",
            )

    # Rule 3: Offensive Language & Insults
    for pattern in OFFENSIVE_PATTERNS:
        if re.search(pattern, lower_query):
            logger.info(
                "Guardrail blocked: Profanity/Offensive language detected (%s)", pattern
            )
            return GuardrailResult(
                is_blocked=True,
                reply="Please use respectful language.",
                category="offensive_language",
            )

    # Rule 4: SQL Injection Patterns
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, lower_query):
            logger.info(
                "Guardrail blocked: SQL injection pattern detected (%s)", pattern
            )
            return GuardrailResult(
                is_blocked=True,
                reply="SQL injection attempt detected. Request rejected.",
                category="sql_injection",
            )

    # Rule 5: PII Detection (Credit Card, CVV, Passwords, Aadhaar, PAN, Passport, OTP, PIN)
    if (
        re.search(PII_CREDIT_CARD_PATTERN, clean_query)
        or re.search(PII_CVV_PATTERN, lower_query)
        or re.search(PII_AADHAAR_PATTERN, clean_query)
        or re.search(PII_PAN_PATTERN, clean_query)
        or any(re.search(pat, lower_query) for pat in PII_KEYWORDS)
    ):
        logger.info("Guardrail blocked: Sensitive PII detected in query")
        return GuardrailResult(
            is_blocked=True,
            reply="Sensitive personal information cannot be processed.",
            category="pii_detected",
        )

    # Rule 6: Sensitive / Unsafe Financial Advice
    for pattern in UNSAFE_ADVICE_PATTERNS:
        if re.search(pattern, lower_query):
            logger.info(
                "Guardrail blocked: Sensitive financial advice query (%s)", pattern
            )
            return GuardrailResult(
                is_blocked=True,
                reply="Sensitive financial advice or guaranteed profit predictions cannot be provided.",
                category="unsafe_financial_advice",
            )

    # Rule 7: Dangerous / Illegal Financial Content
    for pattern in ILLEGAL_FINANCE_PATTERNS:
        if re.search(pattern, lower_query):
            logger.info(
                "Guardrail blocked: Illegal financial practice query (%s)", pattern
            )
            return GuardrailResult(
                is_blocked=True,
                reply="Illegal financial practices, tax fraud, or market manipulation queries are strictly prohibited.",
                category="illegal_financial_content",
            )

    # Rule 8: Document / Database Existence Checks
    asks_for_doc = any(re.search(pat, lower_query) for pat in RESOURCE_DOC_PATTERNS)
    asks_for_sql = any(re.search(pat, lower_query) for pat in RESOURCE_SQL_PATTERNS)

    if (asks_for_doc and not has_documents) or (asks_for_sql and not has_tables):
        logger.info(
            "Guardrail blocked: Query requested documents/SQL tables but none exist"
        )
        return GuardrailResult(
            is_blocked=True,
            reply="No document or Database has been uploaded. Upload SQL Database or Documents First.",
            category="missing_resources",
        )

    # Passed all Guardrails cleanly
    return GuardrailResult(is_blocked=False, reply="")
