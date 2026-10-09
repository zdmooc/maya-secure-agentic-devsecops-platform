# BFI — Matrice exigences, gaps et responsabilités

**Source :** texte d'annonce partagé le 09/10/2026. Aucun client, système ou flux bancaire réel n'a été audité.

| ID | Exigence mission | Existant prouvé / conçu | Gap | Owner |
|---|---|---|---|---|
| BFI-01 | Standards sécurité Responsible AI | Hub architecture IA, D-099 méthode | Déclinaison des contrôles et dérogations en contexte BFI | Ce dossier |
| BFI-02 | Guardrails entrées, RAG, sorties LLM | TradeOps filtrage markers prompt + tests | Cas multi-frontières, DLP et structure de sortie | Module guardrails synthétique, CI |
| BFI-03 | AI Red Team | Secure Agentic roadmap I6 = DESIGNED | Corpus automatisé de scénarios et tests régressifs | Corpus RAI, CI |
| BFI-04 | MCP, least privilege, HITL | TradeOps R3 CI + R5 CRC read-only MQ | Délégation, replay, permission et approbation bornée | Contrat de test ici, runtime D-092 |
| BFI-05 | A2A peer identity | D-092 agent card/JSON-RPC + CI | Authentification du pair et A2A live encore ouverts | D-092 / TradeOps |
| BFI-06 | Agent registry / lifecycle | Hub IA Agent Registry DESIGNED | Instancier les transitions et droits | RAI registry in-memory |
| BFI-07 | Architecture reviews, risques et dérogations | Hub IA architecture review checklist | Rapport de décision avec écarts et risques résiduels | Dossier de revue BFI |
| BFI-08 | IAM, chiffrement, audit et secrets | D-090 G2 sur CRC single-consumer | Enterprise TLS/mTLS, rotation, retention/SIEM | Standards + tests prévus, pas runtime claim |
| BFI-09 | Preuves reproductibles | D-090 G2 / MCP-R5 runtime CRC sur leurs périmètres | Runtime spécifique Responsible AI encore absent | CI + runbook séparé |
| BFI-10 | Guides techniques et gouvernance | Références techniques générales | Pack concentré mission + préparation entretien | Ce dossier |

### Scénario synthétique
L'agent fictif payment-ops lit la santé d'une file MQ et, sur une mutation simulée, exige une approbation signée et liée à l'action, à durée limitée et non rejouable. Aucune transaction bancaire n'est exécutée.

### Décision
Réutiliser les owners existants. Ne pas bloquer D-099, ni réécrire D-092, ni créer de nouveau dépôt. Les questions réglementaires nécessitent qualification du cas d'usage et validation juridique indépendante.
