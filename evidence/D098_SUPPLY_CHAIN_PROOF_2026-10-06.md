# D-098 — SQY-5 Supply-Chain Security Proof — 2026-10-06

**Status:** RUNTIME/CI PROVEN FOR BOUNDED D-098 SCOPE  
**Workflow:** `D098 Supply Chain Proof`  
**Run:** `37517552045`  
**Head:** `e4f73d3e66f4aa1c751273276b2df198ef8c709e`

## Scope

This proof is intentionally isolated from the Agentic AI program.
It validates the generic container supply-chain controls required by D-098.

## OCI image

A disposable scratch OCI image was built from `proofs/d098`, pushed to a disposable local OCI registry,
and addressed by immutable digest.

Observed marker:

`D098_OCI_IMMUTABLE_DIGEST=PASS`.

## Trivy

Trivy version observed:

`0.70.0`.

The disposable OCI image was scanned with vulnerability and secret scanners.

Observed marker:

`D098_TRIVY_IMAGE_SCAN=PASS`.

The JSON scan result is stored in the workflow artifact.

## Cosign

Cosign version observed:

`v2.4.3`.

The immutable image digest was:
1. signed with a disposable D-098 key;
2. verified successfully with the matching public key;
3. verified negatively with an unrelated/untrusted public key.

Observed markers:

```text
D098_COSIGN_SIGN_VERIFY=PASS
D098_COSIGN_UNTRUSTED_NEGATIVE=PASS
D098_COSIGN_IMAGE_VERIFICATION=PASS
```

Private signing keys were deleted before evidence upload.

## Kyverno

Kyverno CLI version pinned by the workflow:

`v1.19.1`.

Policy:
`proofs/d098/kyverno/disallow-latest.yaml`.

Positive fixture:
immutable versioned tag.

Observed summary:

`pass: 1, fail: 0, warn: 0, error: 0, skip: 0`.

Negative fixture:
mutable `:latest` image.

Observed summary:

`pass: 0, fail: 1, warn: 0, error: 0, skip: 0`.

Markers:

```text
D098_KYVERNO_POSITIVE=PASS
D098_KYVERNO_NEGATIVE=PASS
D098_KYVERNO_POLICY_PROOF=PASS
```

## Final result

`D098_SUPPLY_CHAIN_PROOF=PASS`.

Artifact:
`d098-supply-chain-evidence`.

Artifact ID:
`11436989716`.

Artifact digest:
`sha256:70a3351a20f3cb1835e565d59a399a1cd388a258cf7902a2592f17f92c7461a0`.

## Truth boundary

This proves a bounded CI/runtime security chain:
- image scan;
- immutable digest;
- signing;
- positive signature verification;
- negative untrusted verification;
- policy-as-code positive and negative evaluation.

It does not prove:
- production registry integration;
- cluster-side Kyverno admission webhook runtime;
- enterprise key management/HSM;
- keyless workload identity;
- production release governance.

Cluster-side OpenShift admission is evidenced separately by the D-098 SCC positive/negative runtime proof.
