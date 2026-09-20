# OWASP / Agentic Security Mapping

Status: **REFERENCE BASELINE — REFRESH WHEN IMPLEMENTATION RESUMES**

The repository must map final controls to the then-current official OWASP GenAI/LLM and Agentic AI guidance.

Current control families already represented in the design:
- prompt injection;
- sensitive information disclosure / exfiltration;
- supply-chain compromise;
- data/model/knowledge poisoning;
- improper/unsafe output handling;
- excessive agency;
- tool/MCP misuse;
- identity and authorization;
- human oversight;
- provenance and audit.

## Rule

Do not hard-code an old OWASP numbering into the architecture without checking the current official release at implementation time. Threat/control names matter more than stale list numbers.

Final evidence should map:
`Threat -> Control -> Test -> Result -> Evidence`.
