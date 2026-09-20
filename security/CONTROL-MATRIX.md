# Security Control Matrix

Status: **DESIGNED / NOT YET EVIDENCED**

| Layer | Control | Planned mechanism | Evidence |
|---|---|---|---|
| Source | Secrets | Gitleaks/TruffleHog candidate | pending |
| Source | SAST | Semgrep/CodeQL candidate | pending |
| Dependency | SCA/CVE | Trivy/Grype candidate | pending |
| Dependency | License | policy + SBOM review | pending |
| IaC | Terraform/K8s/Helm | Checkov/Trivy config | pending |
| AI | Prompt injection | Promptfoo regression | pending |
| AI | RAG poisoning | curated fixtures + eval | pending |
| AI | Exfiltration | attack fixtures + policy | pending |
| Agent | Excessive agency | bounded autonomy/HITL | pending |
| MCP | Tool authZ | deterministic scopes/policies | pending |
| Build | SBOM | SPDX/CycloneDX | pending |
| Build | AI-BOM | OWASP/project metadata | pending |
| Build | Image CVE | Trivy | pending |
| Build | Provenance | SLSA-oriented attestation | pending |
| Build | Signature | Cosign/Sigstore | pending |
| Deploy | GitOps | Argo CD | pending |
| Admission | Workload policies | Kyverno | pending |
| Runtime | Identity | OIDC/workload identity | pending |
| Runtime | Network | default-deny NetworkPolicy | pending |
| Runtime | Secrets | externalized secret mechanism | pending |
| Runtime | Audit | OTel/security events | pending |
| Human | Approval | separate reviewer identity | pending |

No row may be marked implemented/tested without linked evidence.
