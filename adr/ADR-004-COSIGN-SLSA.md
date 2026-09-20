# ADR-004 — Sign Artifacts and Capture Build Provenance

Status: **PROPOSED**

## Decision
Evaluate Sigstore Cosign for OCI signing/attestation and use SLSA-oriented provenance.

## Rationale
Scanning without artifact identity/provenance leaves a gap between verified source/build and deployed image.

## Acceptance criteria
- image referenced by digest;
- CI identity verifiable;
- signature verification automated;
- deployment gate can reject untrusted artifact;
- key/identity lifecycle documented.
