# Policy-as-Code Catalog

Status: **DESIGNED**

## Admission policies

Planned baseline:
- forbid privileged containers;
- forbid hostPath unless explicitly exempted;
- require resource requests/limits;
- require non-root/restricted security posture where applicable;
- forbid mutable `latest` image tags;
- require approved registries;
- require image digest or approved immutability policy;
- require signature/attestation verification once enabled;
- restrict service-account token automount;
- enforce namespace labels/ownership;
- enforce NetworkPolicy baseline.

## Agent policies

Planned deterministic policy inputs:
- user/workload identity;
- tool;
- requested action;
- data classification;
- autonomy level;
- environment;
- risk level;
- approval state;
- budget/rate limit;
- incident/emergency mode.

Result:
`ALLOW | DENY | REQUIRE_APPROVAL | SAFE_DEGRADED`

## Exception model

Every exception needs:
- owner;
- rationale;
- scope;
- expiry;
- compensating control;
- approval;
- review date.

No permanent anonymous exception.
