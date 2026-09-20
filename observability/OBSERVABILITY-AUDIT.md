# Security Observability and Audit

Status: **DESIGNED**

## Correlation

Target trace context must connect:

`user request -> gateway -> agent -> RAG -> model -> MCP/tool -> policy -> HITL -> deterministic backend`

## Security telemetry

Capture where applicable:
- correlation/trace ID;
- pseudonymous principal/workload;
- agent/workflow version;
- prompt/policy version;
- model alias/version;
- retrieved source IDs, not full sensitive content by default;
- tool requested/called;
- tool policy decision;
- denied reason code;
- approval ID/reviewer identity reference;
- token/cost/latency;
- security scanner/eval result;
- deployment/admission denial.

## Do not log by default

- raw secrets;
- access tokens;
- private keys;
- full sensitive prompts/documents;
- payment/card/customer data not required for diagnosis.

## Dashboard target

A final Grafana/security view should make visible:
- blocked attacks;
- tool denials;
- approval-required actions;
- security gate status;
- runtime errors;
- policy/admission failures.
