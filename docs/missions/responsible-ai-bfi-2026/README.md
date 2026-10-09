# Mission BFI — Responsible AI et sécurité des agents — dossier 2026

**Date : 2026-10-09. Nature : démonstrateur et dossier de sécurité synthétiques, sans données client.**
**Statut : documentations et contrôles CI à vérifier ; aucun runtime CRC prouvé par ce chantier.**

## Objectif
Préparer les livrables d'un architecte Responsible AI : cadre de sécurité, guardrails d'entrée/sortie, sécurité MCP/A2A, gouvernance d'agents, dossier Architecture Review Board et preuves reproductibles d'attaques/refus.

## Ownership et non-chevauchement

| Programme / dépôt | Owner et limite |
|---|---|
| D-099 / maya-ai-agentic-architecture-reference | Agent architecte AA0–AA9 **EN COURS**. Ne pas toucher sa branche active. AA7 pourra réutiliser les tests de sécurité qualifiés ici. |
| D-092 / TradeOps-GenAI-Integration | MCP et A2A ; MCP-R5 prouvé CRC read-only IBM MQ ; A2A live/authentifié toujours ouvert. Aucun fork ni nouveau runtime MCP. |
| maya-secure-agentic-devsecops-platform | Tests, politiques et livrables BFI spécialisés. |
| cadrage_202682030 | Candidature envoyée le 09/10/2026, TJM 600 €, suivi et preuves. |

Le programme générique I0–I12 est distinct : le pack mission ne ferme pas automatiquement ses jalons.

## Documents du dossier
- [Exigences et gaps](REQUIREMENTS_GAP_MATRIX.md)
- [Matrice de contrôles](RESPONSIBLE_AI_CONTROL_MATRIX.md)
- [Guide guardrails](GUARDRAILS_DEPLOYMENT_GUIDE.md)
- [Guide MCP/A2A](MCP_A2A_SECURITY_GUIDE.md)
- [Registre et cycle de vie](AGENT_REGISTRY_REVIEW.md)
- [Rapport de revue architecture](ARCHITECTURE_REVIEW_REPORT.md)
- [Index des preuves](EVIDENCE_INDEX.md)
- [Journal RAI-00 à RAI-07](ITERATION_LEDGER.md)
- [Protocole runtime CRC](CRC_RUNTIME_RUNBOOK.md)

## Implémentations
- Code : [guardrails](../../../rai_bfi/guardrails.py), [autorisation/HITL](../../../rai_bfi/policy.py), [registry](../../../rai_bfi/registry.py).
- [Corpus adversarial](../../../redteam/rai-bfi-2026/attack_cases.json), [tests unittest](../../../tests/test_rai_bfi.py) et workflow GitHub Actions RAI BFI.

Exécution locale : lancer **python -m unittest discover -s tests -p 'test_rai_bfi.py' -v**, puis **python -m scripts.rai_bfi_demo** et **python scripts/rai_bfi_validate.py** depuis la racine.

## Vérité des preuves
DESIGNED ≠ IMPLEMENTED ≠ CI_VERIFIED ≠ CRC_RUNTIME_PROVEN ≠ PRODUCTION_OPERATED. Les patterns lexicaux du module ne sont pas un produit DLP ou un moteur anti-jailbreak complet. Les tests synthétiques ne valident pas le transport A2A, mTLS, la sécurité de production, une conformité juridique ou une transaction financière réelle.
