# Maya Secure Agentic DevSecOps Platform

**Enterprise Secure Agentic DevSecOps Reference Platform**

> From source code, prompts and infrastructure-as-code to a signed software/AI supply chain, governed MCP tools, zero-trust agent runtime and auditable deployment on OpenShift.

## Status

**PROGRAM SCAFFOLD / DESIGN BASELINE — IMPLEMENTATION DEFERRED UNTIL THE CURRENT WERO / INSTANT-PAYMENTS POC IS FINISHED.**

This repository is intentionally created now to capture the complete target scope, architecture, roadmap, controls, ADRs, demo scenario and evidence model. It must **not** be presented as implemented, tested, deployed or production-ready until runtime evidence exists.

## Why this repository exists

The portfolio already contains:

- `maya-ai-agentic-architecture-reference` — canonical Agentic AI architecture/governance hub;
- `TradeOps-GenAI-Integration` — executable RAG/agents/MCP/HITL runtime;
- Wero / instant-payments repositories — payment resilience and deterministic transaction evidence;
- OpenShift / GitOps / Azure / MQ / Kafka specialist repositories.

This repository isolates a missing cross-cutting discipline:

**Agentic DevSecOps + AI Security + Secure Software/AI Supply Chain + Runtime Enforcement.**

It is not another generic AI platform.

## End-to-end target

```text
Developer / AI Engineer
        |
        v
Git / Pull Request
        |
        +--> Secret scanning
        +--> SAST
        +--> SCA / CVE / License
        +--> IaC / Kubernetes / Dockerfile scanning
        +--> SBOM
        +--> AI-BOM
        +--> Prompt / RAG / Agent security tests
        +--> MCP / Tool policy tests
        +--> Red-team regression
        |
        v
Build
        |
        +--> Container scan
        +--> Provenance / attestations
        +--> Signature verification
        |
        v
Secure Merge / Release
        |
        v
Registry
        |
        v
Argo CD / GitOps
        |
        v
OpenShift / Kubernetes
        |
        +--> RBAC / OIDC
        +--> NetworkPolicy
        +--> Kyverno / Policy-as-Code
        +--> Secret management
        +--> Agent / MCP policy enforcement
        +--> Human-in-the-loop
        |
        v
Agent / RAG / MCP Runtime
        |
        v
OpenTelemetry / Prometheus / Grafana / Audit / Evidence
```

## Target security gates

The final demonstrator must be able to prove that at least these attacks or misconfigurations are blocked or escalated:

1. committed secret;
2. vulnerable dependency;
3. insecure source pattern;
4. vulnerable container package;
5. insecure Terraform/Kubernetes/Helm configuration;
6. prompt injection;
7. RAG poisoning / untrusted-context injection;
8. unauthorized MCP/tool invocation;
9. excessive agency / privileged action without approval;
10. data exfiltration attempt;
11. unsafe output handling;
12. unsigned or unverifiable artifact;
13. deployment violating runtime policy;
14. unauthorized network path;
15. privileged payment/remediation action without HITL.

## Reference toolchain

The design baseline evaluates or targets:

| Capability | Candidate tools |
|---|---|
| Secret scanning | Gitleaks, TruffleHog |
| SAST | Semgrep and/or GitHub CodeQL |
| SCA / CVE | Trivy, Grype |
| IaC / K8s security | Checkov, Trivy config |
| SBOM | Syft / Trivy, SPDX or CycloneDX |
| AI-BOM | OWASP GenAI Security Project AIBOM Generator + project-specific metadata |
| AI eval / red team CI | Promptfoo |
| Advanced red team | Microsoft PyRIT, NVIDIA garak where justified |
| MCP security | deterministic authorization + protocol/tool metadata controls + MCP-focused scanning patterns |
| Signing | Sigstore Cosign |
| Provenance | SLSA-oriented attestations |
| Policy-as-Code | Kyverno, OPA where justified |
| GitOps | Argo CD |
| Runtime | Kubernetes / OpenShift |
| Observability | OpenTelemetry, Prometheus, Grafana |

Tool adoption is subject to ADR, license review, maintenance status and actual POC needs.

## Repository map

```text
architecture/       target architecture, SDLC, threat model, runtime security
security/           control matrix and security workstreams
redteam/            AI/agent adversarial testing program
supply-chain/       SBOM, AI-BOM, signatures, provenance
policy-as-code/     admission/runtime policy catalog
platform/           OpenShift/Kubernetes runtime security
gitops/             Argo CD deployment model
observability/      security telemetry and audit model
demo/               Payment Operations Agent security demonstrator
adr/                architecture decisions
evidence/           proof index and claim discipline
docs/               references and supporting material
.github/workflows/  CI/CD implementation area (activated progressively)
scripts/            automation implementation area
```

## Demo domain

The flagship demonstrator will be a **synthetic Payment Operations Agent**.

The agent may investigate a payment incident using RAG, Kafka/MQ status, payment APIs and OpenShift telemetry. Sensitive remediation remains deterministic and gated by authorization and, when required, explicit human approval.

No real banking production system or real customer data is used.

## Program roadmap

See [ROADMAP.md](ROADMAP.md).

Target sequence:

`I0 Architecture -> I1 Secrets -> I2 SAST/SCA -> I3 SBOM -> I4 AI-BOM -> I5 IaC/K8s -> I6 AI Red Team -> I7 MCP Security -> I8 Signing/Provenance -> I9 OpenShift Runtime -> I10 Observability -> I11 Secure Release -> I12 Final Demo`.

## Truth / evidence rules

Allowed status vocabulary:

`PLANNED -> DESIGNED -> IMPLEMENTED -> TESTED -> DEPLOYED -> RUNTIME_VALIDATED`

Rules:

- documentation is not implementation;
- CI green is not a live runtime proof;
- a generated SBOM is not a vulnerability scan;
- a dependency scan is not an AI-BOM;
- CRC single-node is not HA evidence;
- a policy manifest is not enforcement evidence until an admission/runtime test proves it;
- an AI red-team checklist is not a red-team result;
- a signed artifact is not sufficient unless verification is also demonstrated;
- synthetic payment data and POC evidence are not client production experience.

## Relationship to the portfolio

This repository should **reuse** rather than duplicate:

- Agent/RAG/MCP/HITL architecture from `maya-ai-agentic-architecture-reference`;
- executable agent runtime patterns from `TradeOps-GenAI-Integration`;
- payment event and resilience scenarios from Wero / Instant Payments;
- OpenShift, Kafka and IBM MQ evidence from specialist repositories.

## Immediate decision

**Do not start the implementation sprint yet.**

The architecture and backlog are captured now. Implementation resumes after completion of the current Wero / instant-payments POC.
