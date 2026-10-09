# Architecture Review Board — revue synthétique Responsible AI BFI

**Rapport ID : ARB-RAI-BFI-2026-001**  
**Nature : exercice personnel synthétique — pas une revue effectuée chez un client.**  
**Décision : POC REQUIRED / MATERIAL UNCERTAINTY (proposée, NON APPROUVÉE).**  
**Auteur : architecte de solution ; reviewer indépendant : NON DÉSIGNÉ.**

## 1. Périmètre et hypothèses
Cas : agent d'opérations de paiements fictif consultant un état MQ via MCP et dialoguant avec un autre agent en A2A. Mutation métier toujours interdite sans policy déterministe et HITL hors LLM. Architecture de laboratoire seulement, pas un SI BFI connu ni un accès au client.

## 2. Options comparées
| Option | Position | Avantage | Risque / condition |
|---|---|---|---|
| S1 — Guardrails par prompts seuls | REJET PROPOSÉ | Coût faible | Contournable, aucune AuthZ outillée |
| S2 — Gate IAM + policy déterministe + guardrails + HITL | ORIENTATION PROPOSÉE | Testabilité, séparation des responsabilités, audit | IAM, secrets, DLP et démonstration runtime à qualifier |
| S3 — Plateforme managée externe | COMPARAISON PENDING | Service potentiellement intégré | Résidence des données, audit, dépendance fournisseur, coût non instruits |

**Aucune option approuvée :** comparatif contractuel, résidence, NFR et coût réels restent à instruire.

## 3. Findings et risque résiduel
| ID | Sévérité | Finding | Action / owner | État |
|---|---|---|---|---|
| F-01 | HIGH | Prompt injection indirecte et données RAG/tool non fiables | Corpus adversarial élargi + mesure de robustesse, Secure Agentic | CI synthétique seulement |
| F-02 | HIGH | Identité de pair A2A non authentifiée en runtime démontré | Gate A2A transport auth + peer authorization, D-092 owner | OPEN |
| F-03 | HIGH | Validation DLP et sorties non exhaustives | DLP qualifiée par classes + métriques + revues | OPEN |
| F-04 | HIGH | Approvals/révocation non distribuées sur instances multiples | IAM + store atomique + tests replay/timeouts | OPEN |
| F-05 | MEDIUM | Registre en mémoire non gouverné enterprise | Inventaire versionné, owners, approbations, kill switch | DESIGN/DEMO |
| F-06 | MEDIUM | Absence de preuve runtime BFI spécifique | Exécuter runbook CRC + pack expurgé sans impacter D-099 | OPEN |
| F-07 | MEDIUM | Traces sensibles à risque | Minimiser logs, redaction, TTL, accès, contrôle SIEM | DESIGN |

## 4. NFR et acceptation
Exiger résultats de refus pour tentative de tool hors scope, peer forgé, approbation expirée/rejouée, argument modifié, récupération RAG empoisonnée, fuite sensible en sortie, suspension. Enregistrer taux de détection/false positives/false negatives et latence **avant** revendication de performance. NFR de disponibilité, volumétrie, résidence, disponibilité crypto et audit à mesurer ; aucun chiffre inventé.

## 5. Décision sollicitée
**Autoriser uniquement les tests synthétiques et une preuve runtime bornée, après revue humaine du runbook.** Ne pas promouvoir en production. Exiger revues sécurité, conformité, DPO/juridique selon contexte client, exploitation, IAM, propriétaires métiers et architecture board.

Signatures : **AUCUNE**. Rapport démonstratif réutilisable comme modèle d'entretien.
