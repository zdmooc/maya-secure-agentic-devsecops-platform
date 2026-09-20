# ADR-003 — Maintain Both SBOM and AI-BOM

Status: **ACCEPTED AS DESIGN BASELINE**

## Decision
A release will carry both a software SBOM and an AI-specific BOM.

## Rationale
Software packages and CVEs are not enough to reconstruct models, prompts, datasets, indexes and tools.

## Consequence
The release evidence bundle must correlate both BOMs to the same artifact/release identity.
