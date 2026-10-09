# Evidence Index — BFI Responsible AI 2026

## Statuts stricts
- **DESIGNED** : documents et contrats écrits.
- **IMPLEMENTED** : code présent.
- **LOCAL_TESTED** : tests lancés localement avec sortie conservée.
- **CI_VERIFIED** : GitHub Actions exécute avec résultat SUCCESS/commit identifiés.
- **CRC_RUNTIME_PROVEN** : campagne observable avec identifiants, traces, refus et restauration.
- **PRODUCTION_OPERATED** : preuve de production client, **jamais revendiquée dans ce dossier**.

## Inventaire à qualifier
| Artefact | Objet | Claim maximal en l'absence de résultat CI |
|---|---|---|
| rai_bfi/guardrails.py | Entrée RAG, sortie LLM, JSON contrôlé | IMPLEMENTED, heuristique incomplète |
| rai_bfi/policy.py | Tool AuthZ scope/tenant et ticket approbation HMAC | IMPLEMENTED, hors AuthN transport |
| rai_bfi/registry.py | Agent lifecycle en mémoire | IMPLEMENTED |
| redteam/rai-bfi-2026/attack_cases.json | Corpus synthétique d'attaques | DESIGNED |
| tests/test_rai_bfi.py | Scénarios de refus et autorisations unitaires | IMPLEMENTED avant test CI |
| scripts/rai_bfi_validate.py | Contrôle structure documentaire et scénarios | IMPLEMENTED avant test CI |
| .github/workflows/rai-bfi-security.yml | Pipeline automatisé | IMPLEMENTED avant run |
| ARCHITECTURE_REVIEW_REPORT.md | Exemple de revue BFI | DESIGNED, NON SIGNÉ |
| CRC_RUNTIME_RUNBOOK.md | Protocole d'acceptation externe | DESIGNED, NON EXÉCUTÉ |

## Preuves distinctes déjà enregistrées dans les owners
1. D-090 G2 : https://github.com/zdmooc/TradeOps-GenAI-Integration/blob/main/evidence/d090/20261007-g2-crc-runtime-proof.md — policy de modèle, quota et budget sur CRC single-consumer.
2. D-092 MCP-R5 : https://github.com/zdmooc/TradeOps-GenAI-Integration/blob/main/evidence/r5/20261008-crc-native-mcp-mq-observed-summary.md — refus de file MQ système, preuve CRC mono-nœud read-only.
3. A2A D-092 : https://github.com/zdmooc/TradeOps-GenAI-Integration/blob/main/docs/39-a2a-interoperability-d092.md — implémentation/CI ; live peer auth NON PROUVÉE.
4. D-099 : https://github.com/zdmooc/maya-ai-agentic-architecture-reference/tree/d099-aa0-aa2-method-contracts — travail en cours ; benchmark AA3 non homologué.

## Résultat GitHub Actions observé le 09/10/2026

- **Workflow :** Responsible AI BFI - bounded CI ;
- **Run :** https://github.com/zdmooc/maya-secure-agentic-devsecops-platform/actions/runs/37902017400 ;
- **Commit exécuté :** d7242fe8296c4e5ededfd7f3a29b3231e53dbc13 ;
- **Résultat : SUCCESS** — 25 tests unittest **OK** ;
- **Démonstration hors ligne : PASS**, scope SYNTHETIC_OFFLINE_NOT_CRC, neuf décisions positives/négatives attendues ;
- **Validation structure + matrice : PASS**, gate RAI_BFI_STATIC_AND_TEST_CONTRACT ;
- **Portée :** CI Python 3.11, données synthétiques, sans A2A réseau, sans vraie AuthN d'agent, sans outil externe et sans exécution CRC.

Les mises à jour documentaires de ce fichier doivent faire l'objet d'un run CI ultérieur si HEAD change ; ne pas prétendre que le run ci-dessus valide automatiquement une version nouvelle du code. Aucun succès d'un autre dépôt n'est substitué à cette preuve.

## Données et traçabilité
Aucun mot de passe ou token, aucune donnée client, aucun kubeconfig, aucun dump non expurgé ne doit être archivé. SHA des commits, run id, Python version, marqueurs PASS/FAIL et limites de preuve doivent être consignés.
