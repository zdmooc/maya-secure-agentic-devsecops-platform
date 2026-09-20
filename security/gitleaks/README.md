# Secret Scanning Workstream

Status: **PLANNED**

Target first implementation:
- Gitleaks on PR/push;
- synthetic canary secret fixture in a controlled test;
- documented false-positive suppression process;
- fork/secret safety.

Optional comparison: TruffleHog for verification-depth use cases.

Evidence required: a known synthetic secret must block the pipeline without exposing the secret in logs.
