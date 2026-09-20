# Agentic AI Threat Model

Status: **REFERENCE BASELINE / TAILOR PER USE CASE**

## Assets

- source, prompts, policies and tool definitions;
- API/MCP credentials and workload identities;
- models and model endpoints;
- RAG sources, embeddings and indexes;
- build artifacts and registries;
- payment/event/operations data;
- human approvals;
- audit and provenance evidence.

## Threat actors

- malicious external user;
- compromised developer account;
- compromised dependency/tool/model source;
- malicious or poisoned document source;
- compromised MCP server;
- compromised CI runner;
- insider with excessive privilege;
- indirect attacker through third-party content.

## Priority threat scenarios

| ID | Scenario | Required control |
|---|---|---|
| T01 | Secret committed to Git | secret scanner + history response |
| T02 | Vulnerable/malicious dependency | SCA, pinning, provenance, allow/deny policy |
| T03 | Source vulnerability | SAST + review |
| T04 | IaC/K8s misconfiguration | policy scanning + admission |
| T05 | Prompt injection | trust separation + regression + tool auth |
| T06 | Indirect injection via RAG | source governance + context isolation + tool auth |
| T07 | Data exfiltration | classification, DLP, egress/tool policy, audit |
| T08 | RAG poisoning | provenance, quarantine, validation, versioning |
| T09 | Excessive agency | bounded autonomy, least privilege, HITL |
| T10 | Tool poisoning/shadowing | trusted registry/metadata, integrity checks, explicit allowlist |
| T11 | Unauthorized MCP call | workload/user identity + deterministic authZ |
| T12 | Unsafe model output passed to sink | output validation/encoding/schema checks |
| T13 | Compromised build artifact | attestation, signature, immutable digest |
| T14 | Unsigned artifact deployed | admission verification |
| T15 | Cross-namespace lateral movement | NetworkPolicy + service identity |
| T16 | Approval spoofing/self-escalation | separate reviewer identity + binding |
| T17 | Logging sensitive prompt/data | telemetry minimization/redaction |
| T18 | Provider/model substitution | approved aliases/catalog + attestation/config policy |

## Agent-specific rule

Prompt safety is never the sole security boundary. Authorization remains deterministic outside the model.
