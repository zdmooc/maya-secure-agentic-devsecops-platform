# ADR-001 — Layered Security Pipeline

Status: **ACCEPTED AS DESIGN BASELINE**

## Decision
Use layered gates rather than a single scanner.

Layers:
1. secrets;
2. SAST;
3. SCA/CVE/license;
4. IaC/Kubernetes/container configuration;
5. AI/agent security regression;
6. SBOM/AI-BOM;
7. image/package scanning;
8. signing/provenance;
9. admission/runtime policy.

## Rationale
Agentic AI introduces risks that classic AppSec alone does not cover, while AI-specific scanners do not replace software supply-chain controls.

## Consequence
Promotion policy aggregates multiple independent gates. No single green tool means “secure”.
