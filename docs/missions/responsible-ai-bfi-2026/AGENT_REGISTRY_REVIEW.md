# Agent Registry & Lifecycle — BFI Architecture Review

**Provenance :** réutilisation du standard canonique Agent Registry D-092 du hub IA. Ici seule une **fixture en mémoire** permet de vérifier certaines transitions ; ce n'est pas un registre d'entreprise déployé.

## Fiche minimale d'agent
| Attribut | Justification |
|---|---|
| agent_id, version, owner, tenant | Identité stable, traçabilité et responsable |
| business_purpose, data_classification, risk_level | Finalité et qualification du risque |
| allowed_models, mcp_tools, a2a_peers | Inventaire des surfaces d'action |
| scopes, autonomy_ceiling, reviewer_role | Moindre privilège et autonomie bornée |
| policy_version, evidence_ref, last_review | Revue, conformité et historique |
| deployment, SLO, kill_switch, retention | Exploitabilité et arrêt d'urgence |

## Transitions
DESIGN → REGISTERED → APPROVED → DEPLOYED → SUSPENDED → APPROVED (réapprobation) → DEPLOYED ; retrait irréversible **RETIRED**. Une vraie implémentation doit journaliser date, acteur IAM, motif, version de politique, preuve et approbation.

La fixture Python AgentRegistry teste l'interdiction des transitions non autorisées et le refus d'un agent suspendu par PolicyEngine. Elle **ne fournit pas** d'IAM, de persistance, de mécanisme central de révocation, d'approbation client, ni de scheduler de tâches A2A.

## Contrôles de revue
1. Owner métier, technique et sécurité désignés.
2. L'autonomie maximale et les droits explicites sont revus à chaque changement.
3. Nouvel outil, modèle, source sensible ou peer A2A déclenche réévaluation.
4. La suspension retire les droits d'accès et annule les tâches en cours si l'environnement le permet.
5. La mise à la retraite supprime accès et secrets, traite mémoires/données selon retention.
6. Un agent déployé sans propriétaire ou sans audit est une non-conformité bloquante.

## Exemple synthétique
payment-ops v1.0.0, tenant synthetic-bfi ; tool mq.read autorisé ; payment.restart uniquement si reviewer distinct, action exacte signée, ticket valide non rejoué. L'agent de test est fictif : aucun accès à un système bancaire client.
