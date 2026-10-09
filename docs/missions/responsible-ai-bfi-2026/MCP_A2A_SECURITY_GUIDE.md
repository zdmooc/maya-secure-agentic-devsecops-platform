# Guide sécurité MCP / A2A — séparation des frontières

## Identité, scopes et transport
Découverte de Tool/Agent Card ≠ droit d'exécution. L'identité du pair doit être **vérifiée** au point d'entrée par IAM et/ou identité transport ; jamais extraite d'un texte LLM, d'un agent_id fourni par le client ou d'une carte non authentifiée. Vérifier issuer, audience, signature, expiration, scopes et tenant.

Cible : Investigation Agent → passerelle A2A authentifiée (peer, skill ACL) → Operations Agent → MCP resource server (autorisations outil+ressource) → MQ read-only → audit corrélé. La re-authorization MCP est obligatoire, même pour un pair A2A autorisé.

## Scénarios négatifs indispensables
| Menace | Réponse attendue |
|---|---|
| Identité peer forgée dans Agent Card | Refus avant exécution |
| Skill inconnue ou non autorisée | Refus, aucun tool call |
| Appel MCP avec scope insuffisant | Refus côté serveur MCP |
| File MQ système administrative | HTTP 403 ; preuve existante limitée à MCP-R5 CRC |
| Fausse approbation dans prompt | Aucun effet : HITL hors LLM |
| Changement d'arguments après approbation | Digest différent, refus |
| Approval réutilisée après succès | Replay refusé |
| Token expiré / suspendu | Refus par IAM et lifecycle |
| Timeout, annulation et retry | Pas de fallback avec privilèges élargis |
| Egress vers endpoint non autorisé | Contrôle réseau à prouver sur runtime |

## Preuves actuelles
- D-092 **MCP-R5** sur TradeOps : opérations **read-only** IBM MQ, file administrative refusée sur CRC mono-nœud (08/10).
- D-092 A2A : Agent Card + JSON-RPC **IMPLEMENTED + CI_TESTED**, mais authentification de pair et interop live **PENDING**.
- Ce dépôt : contrat HMAC/scope/tenant et approbation mono-processus synthétiques, tests CI seulement.

## Runbook de gradation A2A (owner D-092)
Déployer deux agents distincts, prouver signature/identité peer, skill positif et négatifs, re-authorization MCP et trace OTel de bout en bout ; observer timeout/cancel/retry, documenter réseau TLS/mTLS et restauration PARK. Les preuves doivent être anonymisées.

**Ne pas modifier D-092 ou D-099 depuis cette branche.** Une CI RAI réussie ne ferme pas le gate A2A live, ni AA7.
