# D-100 M3-I3 — Kyverno Kind admission (digest-only)

**Status:** `COMMITTED / CI_PENDING / ADMISSION_NOT_PROVEN / M3_OPEN`.

D-098 Kyverno CLI evaluations and M3-I1/I2 Syft/Grype/Cosign CI are reused. This iteration exercises the **real Kubernetes validating webhook** in a disposable Kind cluster for a digest-only image-reference requirement.

Server-side dry-run requests must prove an image containing `@sha256:` is accepted, that both `:latest` and `:1.36.1` are rejected by Kyverno policy enforcement rather than errors in parsing or networking, and that the rule is strictly scoped to namespace `d100-m3-admission`.

The test digest is intentionally synthetic. Server-side dry-run calls exercise admission but **do not pull or run an image**. Therefore the test is NOT a proof of image content or cryptographic signature verification. The separate Cosign signature denial shown in M3-I2 was a CLI/registry proof, not an admission webhook decision.

A fail-closed script requires `CI=true` and explicit `D100_M3_CI_ONLY=YES`. Unique Kind kubeconfig; unconditional cleanup. No cloud, no CRC, no secret values.

**M3 cannot be globally closed** until Kyverno admission validates trusted signed images and refuses untrusted signatures in a bounded runtime environment. OpenShift SCC admission also remains unproven.
