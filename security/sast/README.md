# SAST Workstream

Status: **PLANNED**

Evaluate Semgrep and/or GitHub CodeQL.

Required coverage:
- application source;
- dangerous subprocess/shell patterns;
- injection/output handling;
- authZ bypass patterns where statically detectable;
- insecure deserialization/configuration patterns.

Ruff/linting does not count as SAST security coverage.
