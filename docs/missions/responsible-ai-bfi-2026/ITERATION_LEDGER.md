# RAI-00 à RAI-07 — journal de livraison mission BFI

**Règle :** éviter tout chevauchement avec D-099 (AA0–AA9) et D-092 (MCP/A2A). Ne fermer une itération qu'après observation de son gate, sans extrapoler un statut CI à CRC.

| Gate | Portée | Critère de sortie | Statut à la création |
|---|---|---|---|
| RAI-00 | Scope et branche isolée | Branched feature; ownership D-099/D-092 explicite | IMPLEMENTED / branche |
| RAI-01 | Exigences/contrôles Responsible AI | Matrice BFI + classification de preuves | DOCUMENTED |
| RAI-02 | Guardrails input/RAG/output | Code + positive/negative CI, limites des regex | CI_VERIFIED / SYNTHETIC_ONLY |
| RAI-03 | Red-team regression | Corpus versionné + tests reproductibles | IMPLEMENTED / CI PENDING |
| RAI-04 | MCP/HITL/A2A security | Scope/tenant/action approval en CI ; A2A live reste D-092 | CI_VERIFIED / SYNTHETIC_ONLY ; A2A LIVE PENDING |
| RAI-05 | Agent Registry + Architecture Review | Contrat lifecycle + revue synthétique et guide | IMPLEMENTED / REVIEW NON SIGNÉ |
| RAI-06 | Audit et evidence pack | Workflow CI SUCCESS rattaché au SHA de branche, limites documentées | CI_VERIFIED / 25 TESTS + OFFLINE DEMO + STATIC CHECKS PASS |
| RAI-07 | Démonstration intégration/runtime | Preuves locales indépendantes sur CRC, consentement opérateur, rollback/PARK | PENDING / EXTERNAL_RUNTIME |

## Preuve disponible

GitHub Actions run 37902017400 (09/10/2026) : SUCCESS, **25/25 tests PASS** ; démonstration hors ligne PASS et validation statique PASS. Ces résultats qualifient les gates du pack comme **CI_VERIFIED**, sauf RAI-07 qui exige une preuve CRC séparée.

## Limites de clôture
RAI-07 peut produire un runbook et une proposition de campagne **sans être CLOSED**. La preuve CRC exige une exécution effective sur un environnement autorisé. Aucun certificat sécurité, conformité AI Act ou validation BFI n'est inféré.

## Convergence
- D-099 poursuit AA3/AA4/AA5... sans dépendance rétroactive.
- Au niveau AA7, importer les références vers les tests de sécurité CI une fois qualifiés ; ne pas dupliquer le pipeline.
- D-092 reste owner des serveurs et protocole A2A/MCP : le pack RAI n'invente pas de second serveur.
- La roadmap générique du dépôt Secure Agentic I0–I12 n'est pas requalifiée artificiellement CLOSED.
