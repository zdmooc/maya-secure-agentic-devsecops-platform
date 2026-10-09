"""Static evidence and control-to-test mapping gate (not a runtime audit)."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "docs/missions/responsible-ai-bfi-2026"

REQUIRED = (
    "README.md", "REQUIREMENTS_GAP_MATRIX.md", "RESPONSIBLE_AI_CONTROL_MATRIX.md",
    "GUARDRAILS_DEPLOYMENT_GUIDE.md", "MCP_A2A_SECURITY_GUIDE.md",
    "AGENT_REGISTRY_REVIEW.md", "ARCHITECTURE_REVIEW_REPORT.md",
    "EVIDENCE_INDEX.md", "ITERATION_LEDGER.md", "CRC_RUNTIME_RUNBOOK.md",
)
CONTROL_IDS = ("RAI-C01", "RAI-C02", "RAI-C03", "RAI-C04", "RAI-C05", "RAI-C06",
               "RAI-C07", "RAI-C08", "RAI-C09", "RAI-C10")
def run():
    issues = []
    for name in REQUIRED:
        p = DIR / name
        if not p.is_file() or len(p.read_text(encoding="utf-8").strip()) < 120:
            issues.append("MISSING_OR_EMPTY:" + name)
    matrix = DIR / "RESPONSIBLE_AI_CONTROL_MATRIX.md"
    if matrix.exists():
        body = matrix.read_text(encoding="utf-8")
        for cid in CONTROL_IDS:
            if cid not in body:
                issues.append("MISSING_CONTROL:" + cid)
    corpus = ROOT / "redteam/rai-bfi-2026/attack_cases.json"
    if not corpus.exists():
        issues.append("MISSING_ATTACK_CORPUS")
    else:
        data = json.loads(corpus.read_text(encoding="utf-8"))
        ids = [c["id"] for c in data["cases"]]
        if len(ids) != len(set(ids)) or len(ids) < 8:
            issues.append("ATTACK_IDS_NOT_UNIQUE_OR_TOO_FEW")
        for case in data["cases"]:
            if case["expected"] not in ("PASS", "SENSITIVE_OUTPUT", "SUSPICIOUS_INSTRUCTION"):
                issues.append("BAD_CASE:" + case["id"])
    print(json.dumps({"gate":"RAI_BFI_STATIC_AND_TEST_CONTRACT",
                      "status":"PASS" if not issues else "FAIL",
                      "controls":len(CONTROL_IDS),"issues":issues,
                      "scope":"SOURCE_AND_CI_ONLY_NOT_CRC"},indent=2))
    return not issues

if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
