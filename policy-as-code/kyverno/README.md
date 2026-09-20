# Kyverno Workstream

Status: **PLANNED**

Target runtime policies:
- require resources;
- require restricted container posture;
- deny privileged/host access;
- deny mutable tags;
- constrain registries;
- require NetworkPolicy baseline;
- verify image signature/attestation when signing is active.

Every policy requires at least one positive and one negative admission test.
