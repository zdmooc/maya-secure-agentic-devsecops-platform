# CI/CD Workflows — Planned

This directory intentionally contains **no active security workflow yet**.

When implementation resumes after the Wero POC, activate workflows incrementally in this order:

1. `secrets.yml`
2. `sast-sca.yml`
3. `iac-security.yml`
4. `sbom-aibom.yml`
5. `ai-security.yml`
6. `container-security.yml`
7. `sign-provenance.yml`
8. `secure-release.yml`

Each workflow must have:
- pinned/reviewed actions where practical;
- least-privilege GitHub token permissions;
- no privileged secrets for untrusted fork PRs;
- versioned output artifacts;
- explicit severity/promotion policy;
- reproducible local or documented equivalent where possible.

Do not add placeholder green jobs and call the capability implemented.
