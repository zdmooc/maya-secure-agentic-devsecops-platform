# OpenShift Runtime Security

Status: **DESIGNED**

## Baseline

The final POC should demonstrate:

- namespace isolation;
- service accounts per workload class;
- least-privilege RBAC;
- restricted container security context;
- explicit CPU/memory resources;
- readiness/liveness/startup probes;
- default-deny NetworkPolicy;
- explicit egress;
- externalized secrets;
- immutable/versioned images;
- Kyverno admission;
- Argo CD delivery;
- observable policy denials.

## Runtime identity

Separate at minimum:
- CI/build identity;
- GitOps controller identity;
- agent workload identity;
- MCP server identity;
- reviewer/human identity;
- backend/service identity.

## Payment domain boundary

An AI agent is not granted direct database/ledger mutation privileges. Sensitive action traverses a deterministic backend API with independent authorization and audit.

## CRC limitation

OpenShift Local / CRC may prove deployment and control behavior, but not multi-worker, multi-AZ, site DR or production capacity.
