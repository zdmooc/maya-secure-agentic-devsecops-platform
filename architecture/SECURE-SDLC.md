# Secure Agentic SDLC

Status: **DESIGNED**

## Lifecycle

### 1. Plan
Define business use case, data classification, agent autonomy, tools, model/provider, threat model, NFR and required evidence.

### 2. Code
Treat source code, prompts, policies, tool schemas, MCP metadata, IaC and evaluation datasets as versioned artifacts.

### 3. Pre-commit / PR
Target gates:
- secret scanning;
- lint/quality;
- SAST;
- dependency/SCA;
- IaC/Kubernetes/Dockerfile checks;
- prompt and agent policy regression.

### 4. Build
Produce immutable artifact, SBOM, AI-BOM and build metadata.

### 5. Verify
Run container/package scan, red-team regression, policy checks and provenance/signature verification.

### 6. Release
Only promote artifacts satisfying the security policy. A green functional test suite alone is insufficient.

### 7. Deploy
Argo CD/GitOps deploys desired state. Admission controls validate image, resource and workload policies.

### 8. Runtime
Enforce identity, network boundaries, tool policies, data controls, HITL and kill/disable mechanisms.

### 9. Observe
Collect trace/correlation, policy decisions, tool calls, denied operations, human approvals, model metadata and security events without leaking sensitive prompt/data content.

### 10. Improve
Security incidents, red-team findings and runtime observations create versioned regression tests.

## Promotion gate model

`FUNCTIONAL_PASS && SECURITY_PASS && AI_SECURITY_PASS && SUPPLY_CHAIN_PASS && POLICY_PASS -> PROMOTABLE`

Any blocking gate produces `NOT_PROMOTABLE`.

## Branch/PR principle

Untrusted fork PRs must never gain access to privileged secrets, signing identities, cloud credentials or local self-hosted runners.
