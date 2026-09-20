# AI Software Supply Chain

Status: **DESIGNED**

## Supply-chain objects

A complete AI delivery chain may contain:

- application source;
- dependencies;
- base/container images;
- Terraform/Helm/Kustomize/Kubernetes;
- prompts/system instructions;
- evaluation datasets;
- RAG corpora;
- embedding models;
- LLM/model identifiers and providers;
- MCP server packages and tool schemas;
- policies/guardrails;
- generated SBOM and AI-BOM;
- OCI artifacts, signatures and attestations.

## Required traceability

For a released demonstrator, be able to answer:

1. Which commit produced this image?
2. Which workflow/build identity produced it?
3. Which dependencies and licenses were included?
4. Which model/provider/prompt/tool versions were associated?
5. Which scans/evals passed?
6. Was the artifact signed?
7. Can deployment verify provenance/signature?
8. Which policy version admitted the workload?

## SBOM vs AI-BOM

**SBOM**: software packages, versions, licenses, file/package relationships.

**AI-BOM** adds AI-specific lineage such as:
- model/provider/version;
- prompt/system-policy version;
- embeddings/index versions;
- datasets/corpora;
- tools/MCP servers;
- evaluation set version;
- ownership, license and provenance.

Generating one does not replace the other.

## Target release bundle

```text
image@sha256:...
sbom.spdx.json
aibom.cdx.json
security-results/
eval-results/
provenance.json
signature/attestation
release-evidence.json
```
