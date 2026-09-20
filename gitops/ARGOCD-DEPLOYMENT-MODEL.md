# Argo CD Deployment Model

Status: **DESIGNED**

## Flow

```text
Application source
  -> CI security/eval gates
  -> build image
  -> scan / SBOM / AI-BOM
  -> sign / attest
  -> release manifest update
  -> GitOps repository/state
  -> Argo CD
  -> admission policies
  -> OpenShift
```

## Separation of duties

- application CI should not directly mutate the cluster;
- Argo CD reconciles declared desired state;
- signing identity is not the runtime identity;
- privileged deployment changes require review;
- policy exceptions are versioned.

## Rollback

Rollback must identify:
- previous trusted image digest;
- matching configuration/prompt/policy versions;
- schema compatibility;
- RAG/index compatibility where relevant;
- verification evidence.

A Git revert alone may be insufficient if stateful AI artifacts changed.
