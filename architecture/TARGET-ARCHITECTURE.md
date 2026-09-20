# Target Architecture

Status: **DESIGNED**

```text
Developer / AI Engineer
  |
  v
Git / Pull Request
  |
  +--> Secret Scan
  +--> SAST
  +--> SCA / CVE / License
  +--> IaC / K8s / Dockerfile Scan
  +--> SBOM
  +--> AI-BOM
  +--> Prompt/RAG/Agent Red Team
  +--> MCP/Tool Authorization Tests
  |
  v
Build
  |
  +--> Container Scan
  +--> Provenance / Attestation
  +--> Signature
  |
  v
Release Gate
  |
  v
OCI Registry
  |
  v
Argo CD
  |
  v
OpenShift / Kubernetes
  |
  +--> Admission Policy
  +--> Signature Verification
  +--> RBAC / Workload Identity
  +--> NetworkPolicy
  +--> Secret Management
  |
  v
Agent Runtime
  |
  +--> RAG / Knowledge
  +--> Model / AI Gateway
  +--> MCP / Tools
  +--> Kafka / MQ / APIs
  |
  +--> Deterministic Policy/Veto
  +--> HITL for sensitive action
  |
  v
Business action boundary
  |
  v
OTel -> Metrics -> Logs -> Audit -> Evidence
```

## Trust zones

1. Developer workstation / source.
2. Git hosting and PR controls.
3. CI execution environment.
4. Build and artifact registry.
5. GitOps control plane.
6. OpenShift platform.
7. AI runtime plane.
8. MCP/tool/integration plane.
9. deterministic business execution plane.
10. evidence/observability plane.

## Architectural invariants

- LLM output cannot grant authorization.
- Tool authorization is server-side and deterministic.
- Sensitive actions require explicit policy and, where required, human approval.
- Untrusted RAG content is data, not instruction.
- Build identity and runtime identity are separate.
- Secrets are not committed to Git.
- Deployment may reject unsigned/untrusted artifacts.
- Every sensitive tool call is correlated and auditable.
- Failure or ambiguity in authorization fails closed.
- Payment/remediation execution remains deterministic.
