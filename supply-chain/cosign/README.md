# Cosign / Sigstore Workstream

Status: **PLANNED**

Target proof:
1. build immutable image;
2. scan image;
3. sign/attest image digest;
4. verify identity/signature;
5. reject tampered/untrusted digest;
6. feed verification into deployment/admission policy.

Keyless/OIDC signing is preferred where the environment and threat model support it.
