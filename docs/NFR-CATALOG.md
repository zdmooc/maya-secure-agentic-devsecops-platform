# Non-Functional Requirements Catalog

Status: **REFERENCE BASELINE**

## Security
- least privilege;
- fail closed on authorization ambiguity;
- no secrets in Git;
- verifiable artifact provenance;
- deterministic tool authorization;
- controlled egress;
- protected sensitive logs.

## Auditability
- every sensitive action traceable to identity, policy, tool, approval and artifact version;
- release evidence reproducible from commit/build metadata.

## Resilience
- safe degraded mode when model/RAG/tool unavailable;
- sensitive action blocked if approval/policy service unavailable;
- rollback path for application + prompt + policy + model/index configuration.

## Performance
- security gates must expose execution time;
- runtime security controls must have measurable latency overhead;
- tool and model timeouts explicit.

## Portability
- avoid coupling core policies to one model provider;
- Kubernetes/OpenShift manifests remain separable from cloud-specific implementation.

## Operability
- runbooks for security gate failure, signature failure, scanner outage, policy denial storm, compromised credential, poisoned knowledge source and MCP tool compromise.

## Cost
- CI/red-team frequency balanced by risk;
- expensive model-based tests may run in tiered pipelines;
- cost evidence separated from estimates.
