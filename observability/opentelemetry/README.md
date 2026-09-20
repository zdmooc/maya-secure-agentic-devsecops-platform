# OpenTelemetry Workstream

Status: **PLANNED**

Target spans/events:
- inbound request;
- RAG retrieval;
- model invocation;
- policy decision;
- MCP/tool call;
- human approval;
- deterministic backend action.

Security attributes must avoid secret/prompt leakage. Correlation should reach Kafka/MQ/API identifiers when the demo uses them.
