# ADR-006 — MCP/Tool Authorization Must Be Deterministic

Status: **ACCEPTED**

## Decision
The model/agent never grants itself tool authority.

Authorization is evaluated outside the LLM from identity, tool, arguments, data classification, environment, autonomy level and approval state.

## Consequence
A prompt injection may influence requested intent, but cannot directly bypass server-side authorization.
