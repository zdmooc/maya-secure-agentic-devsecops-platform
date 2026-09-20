# Argo CD Workstream

Status: **PLANNED**

Desired end state:
- CI builds/verifies artifacts;
- GitOps state references trusted immutable image;
- Argo CD reconciles;
- admission controls validate;
- rollback uses a previously trusted release bundle.

No direct `kubectl apply`/manual drift is part of the final normal release path, except controlled bootstrap/debug evidence.
