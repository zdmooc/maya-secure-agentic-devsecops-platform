# Evidence Index

Status: **EMPTY BY DESIGN UNTIL IMPLEMENTATION STARTS**

Evidence must be reproducible and tied to a commit/version.

Planned structure:

```text
evidence/
  i01-secrets/
  i02-sast-sca/
  i03-sbom/
  i04-aibom/
  i05-iac/
  i06-redteam/
  i07-mcp/
  i08-signing-provenance/
  i09-openshift/
  i10-observability/
  i11-secure-release/
  i12-final-demo/
```

Each evidence record should include:

- date/time;
- git commit SHA;
- tool and version;
- command/workflow;
- input fixture;
- expected result;
- actual result;
- PASS/FAIL;
- raw artifact/log location;
- limitations/non-claims.

Screenshots alone are supporting evidence, not the primary machine-verifiable proof.
