# Matrice de contrôles Responsible AI — démonstrateur synthétique

La mention d'un contrôle ne signifie **ni** qu'il est complet **ni** qu'il est déployé.

| ID | Risque | Règle | Contrôle/test | Limite / preuve |
|---|---|---|---|---|
| RAI-C01 | Injection directe | Refuser motifs suspects, tracer sans contenu sensible | evaluate_text, RI-03 | Heuristique partielle, CI |
| RAI-C02 | Injection RAG / tool output | Sources externes = données non fiables, refus des marqueurs connus | RI-01, RI-02, RI-08 | Attaques nouvelles non exhaustives |
| RAI-C03 | Fuite en sortie | Détection motifs e-mail, clé privée et affectation secret | RI-04, RI-05, test_private_key_and_email | Pas un moteur DLP |
| RAI-C04 | JSON malveillant | Schéma fermé, enum, citation nécessaire, aucune action par JSON brut | validate_structured_answer, test_strict_output_schema | Règles métier indépendantes nécessaires |
| RAI-C05 | Confused deputy | IdP amont, scope/tenant/tool validés par moteur déterministe | PolicyEngine, test_reject_identity_and_tenant, test_reject_tools_and_scopes | AuthN amont non implémentée ici |
| RAI-C06 | Action privilégiée non approuvée | HITL hors LLM, ticket HMAC lié à action et reviewer | mint_approval, test_mutation_needs_review | Approbation simulée |
| RAI-C07 | Replay et mutation non autorisée | Refus signature invalide, hash modifié, expiration, nonce consommé | test_valid_ticket_then_replay_denied, test_argument_escalation_rejected | Store in-memory mono-processus |
| RAI-C08 | Agent obsolète | Cycle DESIGN->REGISTERED->APPROVED->DEPLOYED->SUSPENDED->RETIRED, suspension bloquante | AgentRegistry, test_agent_suspension | Pas de registre distribué |
| RAI-C09 | Peer A2A usurpé | Authentification de l'identité peer côté serveur puis re-authorization MCP | Guide MCP/A2A, gate D-092 | A2A LIVE = PENDING |
| RAI-C10 | Faux claim de sécurité | Niveau d'évidence, revue indépendante, risques résiduels | Evidence Index, Architecture Review Report, validation statique | Rapport client = exemple non signé |

## Politique de qualification
- Toujours rapporter false positives, false negatives, couverture et performance ; ces métriques **ne sont pas mesurées** par la suite actuelle.
- Le modèle ne possède ni clé HMAC ni droit de signer sa propre approbation.
- Une permission A2A ne vaut jamais permission MCP.
- Source d'autorité : IAM, serveur de politique, système métier, révocation, puis audit.
- L'AI Act, le RGPD et DORA ne s'appliquent pas uniformément à tous les cas : qualification et avis juridique requis.
- La CI exécute des tests de contrats synthétiques. La revue de risque et le runtime CRC restent distincts.
