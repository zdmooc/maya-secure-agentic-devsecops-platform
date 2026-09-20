# Roadmap — Secure Agentic DevSecOps Platform

Status: **PLANNED / DESIGN BASELINE**

Implementation is deliberately deferred until the current Wero / instant-payments POC is finished.

## Delivery rule

Every iteration follows:

`ANALYSE -> ARCHITECTURE -> ADR -> IMPLEMENT -> NEGATIVE TEST -> EVIDENCE -> DOCUMENT -> COMMIT -> REVIEW`

No status is upgraded without evidence.

| Iteration | Scope | Exit evidence |
|---|---|---|
| I0 | Architecture, NFR, threat model, control matrix | architecture pack + ADRs + attack surface |
| I1 | Secret interception | synthetic committed secret blocked in PR/CI |
| I2 | SAST + SCA/CVE/license | vulnerable code/dependency blocked with documented policy |
| I3 | SBOM | reproducible SPDX/CycloneDX artifact tied to build |
| I4 | AI-BOM | model/prompt/tool/dataset/index/provider inventory with provenance |
| I5 | IaC/K8s/Dockerfile security | intentionally insecure manifest/Terraform blocked |
| I6 | AI red-team regression | repeatable prompt injection, exfiltration, poisoning, output-abuse, excessive-agency tests |
| I7 | MCP/tool security | unauthorized tool call denied; tool metadata/integrity tests; HITL-required action proven |
| I8 | Artifact signing + provenance | image signed and verified; provenance/attestation attached |
| I9 | OpenShift runtime security | RBAC, NetworkPolicy, Kyverno, secret handling and denial tests on runtime |
| I10 | Observability/audit | end-to-end trace from request to agent/tool/policy/approval |
| I11 | Secure release | PR gates -> build -> attest/sign -> registry -> GitOps -> admission verify |
| I12 | Final adversarial demo | attack matrix executed live with PASS/BLOCK/ESCALATE evidence |

## I0 — Architecture baseline

Deliverables:
- target architecture;
- secure SDLC;
- threat model;
- AI supply-chain model;
- MCP runtime security model;
- NFR and security control matrix;
- ADR baseline;
- evidence model.

Status: **DESIGNED by repository scaffold; implementation not started.**

## Implementation order after Wero

1. establish a minimal synthetic Payment Operations Agent fixture;
2. wire secret/SAST/SCA/IaC gates;
3. generate SBOM and AI-BOM;
4. add Promptfoo-based AI security regression;
5. add MCP/tool authorization attacks;
6. build and scan image;
7. add Cosign/SLSA-oriented attestations;
8. deploy to OpenShift/CRC;
9. enforce Kyverno/NetworkPolicy/RBAC;
10. add OTel/Prometheus/Grafana evidence;
11. package final demo.

## Non-goals

- no real payment execution;
- no customer data;
- no claim of production certification;
- no replacement of the canonical Agentic AI architecture hub;
- no duplication of Wero/MQ/Kafka/OpenShift specialist repositories.
