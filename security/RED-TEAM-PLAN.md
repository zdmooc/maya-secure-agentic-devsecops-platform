# Agentic AI Red-Team Plan

Status: **PLANNED**

## Objective

Create repeatable adversarial tests that can run in CI and, for selected scenarios, against the deployed runtime.

## Test families

1. direct prompt injection;
2. indirect prompt injection from RAG content;
3. jailbreak attempts;
4. sensitive-data extraction;
5. cross-role/ACL bypass;
6. malicious/poisoned knowledge source;
7. tool argument manipulation;
8. unknown/hidden tool invocation;
9. excessive-agency attempt;
10. approval bypass/self-escalation;
11. unsafe output passed to downstream sink;
12. denial-of-wallet/token abuse;
13. tool metadata poisoning/shadowing;
14. compromised dependency/supply-chain fixture.

## Result states

- `BLOCKED`
- `REQUIRES_APPROVAL`
- `SAFE_DEGRADED`
- `ALLOWED_AS_DESIGNED`
- `FAIL`

## CI policy

A regression that changes an expected `BLOCKED` or `REQUIRES_APPROVAL` scenario into an unauthorized `ALLOWED` state blocks promotion.

## Tools

Promptfoo is the default CI-oriented candidate. PyRIT and/or garak are optional deeper campaign tools when they add unique evidence.
