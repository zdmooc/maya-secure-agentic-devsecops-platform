# ADR-005 — Kyverno for Kubernetes/OpenShift Admission Baseline

Status: **PROPOSED**

## Decision
Use Kyverno as the first admission-policy candidate because it aligns with existing portfolio patterns.

## Candidate policies
- resource requests/limits;
- security context;
- no mutable latest tag;
- approved registry/digest;
- NetworkPolicy baseline;
- signature/attestation verification when enabled.

OPA may complement where a use case needs broader policy evaluation.
