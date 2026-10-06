# D-098 — Reusable CaaS Security / Supply-Chain Controls

**Status:** DESIGN_REUSE_READY / RUNTIME ENFORCEMENT PENDING

## Purpose

D-098 reuses only the generic container/Kubernetes supply-chain controls from this repository.
It does **not** pull the Agentic AI security scope into the SQY CaaS mission.

## Controls reused for the CaaS mission

### Build / image security
- Trivy image and configuration scanning;
- optional Grype comparison;
- SBOM generation;
- immutable image references / digest use;
- Cosign signature/attestation pattern.

### Admission / runtime policy
- Kyverno baseline;
- disallow privileged workloads;
- restrict mutable `latest`;
- require requests/limits and probes;
- approved registry/digest;
- signature/attestation verification when implemented;
- observable admission denials.

### Delivery
- Argo CD / GitOps promotion;
- policy changes versioned in Git;
- no secret committed in repository;
- exception process documented.

## D-098 target flow

~~~text
Source / Manifest
    -> scan
    -> build
    -> image scan + SBOM
    -> sign / attest
    -> registry
    -> Argo CD
    -> Kyverno admission
    -> OpenShift
    -> policy denial / runtime evidence
~~~

## Minimum runtime proof for SQY-5

Use a disposable fixture and prove:
1. a compliant image/manifests pass;
2. a known policy violation is denied;
3. an unsigned/untrusted image is denied **only if** Cosign verification is actually wired;
4. Trivy result is captured;
5. Argo/application health is revalidated after the test.

## Truth boundary

The existing Agentic DevSecOps program is not promoted to runtime-proven by D-098.
Cosign/Kyverno manifests or ADRs alone are not enforcement evidence.

## Gate contribution

This document prepares the security part of:
`CAAS_SECOPS_OBSERVABILITY_PACK_READY`.
