# ADR-002 — Promptfoo First for CI-Oriented AI Security

Status: **PROPOSED**

## Decision
Evaluate Promptfoo as the first CI-oriented red-team/evaluation tool.

## Rationale
It is suitable for repeatable prompt/RAG/agent regression and fits CI/CD. PyRIT/garak remain optional for deeper campaigns.

## Acceptance criteria
- supports our target endpoint/workflow;
- can run deterministic fixtures;
- returns machine-readable results;
- negative tests can block promotion;
- license/maintenance posture accepted.

No adoption claim until evaluated.
