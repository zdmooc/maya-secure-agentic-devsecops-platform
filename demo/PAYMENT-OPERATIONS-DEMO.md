# Final Demonstrator — Secure Payment Operations Agent

Status: **PLANNED**

## Purpose

Demonstrate the complete discipline on a synthetic banking/payment incident without real customer data or real money.

## Scenario

A payment is in an ambiguous operational state. The agent may:

- read synthetic payment status;
- inspect Kafka/MQ event history;
- query logs/metrics;
- retrieve approved runbooks through RAG;
- formulate an evidence-backed hypothesis;
- recommend a remediation;
- request a bounded action through MCP/tool boundary.

Sensitive action is never executed merely because the model asks for it.

## Positive journey

1. operator authenticates;
2. agent gathers evidence;
3. RAG returns cited procedure;
4. read-only tools succeed;
5. agent recommends action;
6. policy marks action `REQUIRES_APPROVAL`;
7. reviewer approves;
8. deterministic synthetic backend executes;
9. audit trace proves the whole chain.

## Adversarial journey

Run deliberate attacks:
- hidden prompt injection in a runbook;
- unauthorized tool request;
- manipulated tool arguments;
- agent attempts to bypass approval;
- poisoned document;
- data-exfiltration request;
- unsigned image admission attempt;
- network call outside allowlist.

Expected outcome: `BLOCKED`, `REQUIRES_APPROVAL` or `SAFE_DEGRADED`.

## Demo screen

Future visual cockpit:
- left: operator/payment incident;
- center: agent reasoning summary/evidence/actions (not hidden chain-of-thought);
- right: security gates, policy decisions, traces and alerts;
- bottom: supply-chain status for the deployed release.
