"""Small deterministic guardrail baseline with documented detection limits.

Text matching is defense-in-depth, never a security authority for executing
tools. Production needs model-specific evaluations, classifiers, DLP services,
human review and validated data-handling policies.
"""
from __future__ import annotations
import json
import re
import unicodedata
from dataclasses import dataclass

INJECTION = (
    re.compile(r"ignore\s+(?:all\s+|any\s+)?(?:previous|prior|above)\s+(?:system\s+)?instructions?", re.I),
    re.compile(r"(?:reveal|print|dump|show)\s+(?:the\s+)?(?:hidden\s+)?(?:system\s+)?prompt", re.I),
    re.compile(r"(?:bypass|disable|turn\s+off)\s+(?:the\s+)?(?:safety|security|policy|guardrails?)", re.I),
    re.compile(r"(?:exfiltrat\w*|send|post)\s+.{0,64}(?:secrets?|credentials?|private\s+keys?|api\s+keys?)", re.I),
)
OUTPUT_DLP = (
    ("EMAIL", re.compile(r"\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b", re.I)),
    ("SECRET_ASSIGNMENT", re.compile(r"\b(?:password|api[_-]?key|access[_-]?token)\s*[:=]\s*[^\s,}]{5,}", re.I)),
    ("PRIVATE_KEY", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.I)),
)
ALLOWED_STATES = frozenset({"ANSWER", "ABSTAIN", "ESCALATE"})

@dataclass(frozen=True)
class GuardrailResult:
    allowed: bool
    code: str
    indicators: tuple[str, ...] = ()

def _normalize(text: str) -> str:
    # Remove zero-width formatting before applying bounded deterministic patterns.
    return "".join(ch for ch in unicodedata.normalize("NFKC", text)
                   if unicodedata.category(ch) != "Cf").casefold()

def evaluate_text(text: object, *, boundary: str, max_chars: int = 6000) -> GuardrailResult:
    if boundary not in ("user_input", "retrieval", "tool_result", "llm_output"):
        return GuardrailResult(False, "UNSUPPORTED_BOUNDARY")
    if not isinstance(text, str) or not text.strip():
        return GuardrailResult(False, "EMPTY_OR_INVALID")
    if len(text) > max_chars:
        return GuardrailResult(False, "SIZE_LIMIT")
    if any(ord(ch) < 32 and ch not in "\r\n\t" for ch in text):
        return GuardrailResult(False, "CONTROL_CHARACTER")
    normalized = _normalize(text)
    if boundary in ("user_input", "retrieval", "tool_result"):
        hits = tuple("INJECTION_" + str(i + 1) for i, pattern in enumerate(INJECTION)
                     if pattern.search(normalized))
        if hits:
            return GuardrailResult(False, "SUSPICIOUS_INSTRUCTION", hits)
    if boundary in ("tool_result", "llm_output"):
        findings = tuple(name for name, pattern in OUTPUT_DLP if pattern.search(normalized))
        if findings:
            return GuardrailResult(False, "SENSITIVE_OUTPUT", findings)
    return GuardrailResult(True, "PASS")

def validate_structured_answer(value: object) -> GuardrailResult:
    """Strict typed output contract. No automatic trust in a model's JSON."""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            return GuardrailResult(False, "INVALID_JSON")
    if not isinstance(value, dict) or set(value) != {"status", "answer", "evidence_refs"}:
        return GuardrailResult(False, "SCHEMA_MISMATCH")
    if not isinstance(value["status"], str) or value["status"] not in ALLOWED_STATES:
        return GuardrailResult(False, "INVALID_STATUS")
    if not isinstance(value["answer"], str):
        return GuardrailResult(False, "INVALID_ANSWER")
    if not isinstance(value["evidence_refs"], list) or len(value["evidence_refs"]) > 8 or any(
        not isinstance(x, str) or not x.startswith("repo:") or len(x) > 240
        for x in value["evidence_refs"]
    ):
        return GuardrailResult(False, "INVALID_EVIDENCE")
    if value["status"] == "ANSWER" and not value["evidence_refs"]:
        return GuardrailResult(False, "MISSING_GROUNDING")
    return evaluate_text(value["answer"], boundary="llm_output")
