# IaC / Kubernetes / Dockerfile Security Workstream

Status: **PLANNED**

Candidate baseline:
- Checkov and/or Trivy config;
- Terraform plan/config scanning;
- Kubernetes/Helm/Kustomize scanning;
- Dockerfile hardening checks;
- GitHub Actions workflow review.

Required negative fixtures:
- public exposure;
- privileged container;
- missing resource/security controls;
- wildcard RBAC;
- dangerous egress;
- weak cloud/IaC configuration.

Severity and exception policy must be explicit before blocking production-style promotion.
