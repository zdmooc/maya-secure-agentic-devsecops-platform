# MCP / Tool Runtime Security

Status: **DESIGNED**

## Security boundary

```text
User / Workload Identity
        |
        v
Agent / Orchestrator
        |
        v
Tool Policy Enforcement
  - identity
  - scope
  - argument schema
  - data classification
  - rate/budget
  - autonomy level
  - approval requirement
        |
        +--> DENY
        +--> REQUIRE_APPROVAL
        +--> ALLOW
        |
        v
MCP Server / API Adapter
        |
        v
Deterministic Backend
```

## Controls

- explicit tool allowlist;
- deny unknown tools/arguments;
- strong input schema validation;
- no authorization decision delegated to the LLM;
- per-tool minimum scope/role;
- per-tool autonomy ceiling;
- separate reviewer identity for HITL;
- timeout/rate/budget limits;
- idempotency for side effects;
- dry-run where possible;
- output schema and content validation;
- correlation/audit on every call;
- tool metadata/version integrity checks;
- disable/kill switch for risky tools.

## Payment demo autonomy

- L0/L1: read-only investigation may be automatic.
- L2: bounded reversible operation may require approval depending on risk.
- L3+: financial or production-impacting action is not autonomous in the POC.

The agent may recommend an action; the deterministic backend performs it only after policy and approval conditions pass.
