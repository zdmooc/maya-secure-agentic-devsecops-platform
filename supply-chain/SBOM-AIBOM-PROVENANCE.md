# SBOM, AI-BOM, Provenance and Signing

Status: **DESIGNED**

## Objective

Make every release reconstructable and verifiable.

## Required artifacts

### SBOM
Preferred output: SPDX or CycloneDX.

Minimum:
- package name/version;
- direct/transitive dependency relationship where available;
- license metadata;
- source/image digest.

### AI-BOM
Minimum target fields:
- model/provider/model version or immutable identifier;
- prompt/system-policy version;
- agent/workflow version;
- tools and MCP servers;
- RAG corpus/index/embedding versions;
- evaluation dataset version;
- owners;
- license/usage constraints;
- provenance/source.

### Provenance
Capture:
- source repository;
- commit SHA;
- workflow/build identity;
- build timestamp;
- builder/workflow reference;
- produced artifact digest.

### Signing
Target:
- sign immutable OCI digest;
- verify signature before promotion/deployment;
- prefer short-lived/keyless identity where the environment supports it;
- record verification result in evidence.

## Verification principle

A release is not trusted because it came from a trusted repository. Trust is derived from verifiable source, build, artifact and policy evidence.
