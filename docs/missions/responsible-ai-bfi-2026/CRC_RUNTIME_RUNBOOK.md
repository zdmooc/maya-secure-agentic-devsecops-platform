# Gate RAI-07 — protocole de vérification OpenShift Local / CRC (NON EXÉCUTÉ)

**Objectif :** expliquer comment obtenir une preuve reproductible et sûre, sans attribuer une validation CRC à des tests purement GitHub. Ce runbook est une proposition qui exige revue de l'opérateur habilité.

## Préconditions
1. Vérifier contexte OpenShift, namespace et absence de session D-099 sensible ; D-099 est **en cours**.
2. Vérifier les contrats de D-092 et que son owner a autorisé la fenêtre read-only ; aucun accès implicite accordé par ce document.
3. Capture d'un inventaire READ-ONLY : version cluster, namespaces pertinents, déploiements, quotas, capacité, PARK state.
4. Aucun secret brut, token, kubeconfig ou donnée client dans la sortie ; base de tests synthétiques exclusivement.
5. Ne pas lancer de cluster, n'activer aucun pod, aucune commande mutatrice ou GitOps depuis le présent dépôt sans plan séparé approuvé.

## Première passe sans CRC
Depuis le dépôt secure :
- python -m unittest discover -s tests -p 'test_rai_bfi.py' -v
- python scripts/rai_bfi_validate.py
- Vérifier commit SHA, Python, CI, taux PASS/FAIL et limites du corpus.

## Runtime cible à faire valider par les owners D-092/TradeOps
1. Prouver l'identité peer réelle et le refus d'Agent Card frauduleuse.
2. Exécuter A2A skill positif + négatifs de peer/skill.
3. Tracer la re-authorization MCP en aval et l'accès MQ read-only.
4. Refuser modifications de paramètres après approbation, tickets expirés/rejoués.
5. Refuser exfiltration et tool metadata injection ; produire un audit sans PII.
6. Mesurer la portée, les versions, les latences et les limitations CRC mono-nœud.
7. Restaurer PARK ou état initial ; démontrer état final comparé.

## Acceptation
Ne déclarer RAI-07 CRC_RUNTIME_PROVEN qu'en présence de preuves live avec protocole, commits, identités non sensibles, horodatages, résultats positifs/négatifs, état initial/final, hashes et reviewer distinct. Sinon **RAI-07=PENDING**.

Le script RAI n'exécute pas automatiquement de commande oc, helm, Argo CD ou IBM MQ. Il ne peut pas modifier le poste de l'utilisateur ni la branche D-099.
