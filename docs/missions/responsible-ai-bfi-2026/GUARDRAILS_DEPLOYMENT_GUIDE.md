# Guide de déploiement — guardrails entrée/RAG/sortie

## Chaîne d'architecture cible (DESIGNED)

1. Gateway valide l'identité, l'audience, les scopes, le tenant, rate limit et budget.
2. Classifier finalité et classes de données, appliquer droits de résidence et rétention.
3. Filtrer entrée utilisateur puis contexte RAG/tool depuis sources non fiables ; ACL appliquées **avant** retrieval.
4. Appeler le LLM autorisé, avec prompt et modèle versionnés, sans secrets dans le prompt.
5. Valider la structure de réponse ; contrôler fuites de données et politiques de sûreté.
6. Recontrôler toute action métier avec une règle déterministe et, si sensible, HITL côté serveur.
7. Exporter seulement des données d'audit minimales, sans texte de prompt, secret ni document sensible.

Exemple code depuis racine du dépôt :

    from rai_bfi.guardrails import evaluate_text, validate_structured_answer
    assert evaluate_text("Diagnostic MQ", boundary="user_input").allowed
    assert evaluate_text("Documentation connue", boundary="retrieval").allowed
    verdict = validate_structured_answer({
        "status": "ANSWER", "answer": "Diagnostic autorisé.",
        "evidence_refs": ["repo:synthetic/source.md"]
    })
    assert verdict.allowed

## Contrôles fail-closed
- Erreur parsing : refus.
- Taille hors budget / caractère de contrôle : refus.
- Instruction malveillante connue dans RAG : refus de confiance.
- Donnée sensible détectée dans sortie : refuser la diffusion, demander redaction/revue.
- JSON valide mais outil demandé sans scopes : refus par PolicyEngine **indépendant** des guardrails.

## Limites explicites
Les regex de la démo ne couvrent ni prompt injections polyglottes, ni attaques de faible similarité, ni identification exhaustive de PII, ni toutes les langues. Les faux négatifs et faux positifs restent **non mesurés**. Ce n'est pas un pare-feu LLM de production.

## Industrialisation future
Mettre en place corpus de validation représentatif, DLP/PII, mesure précision/rappel/latence/coût, chemins d'escalade, data residency, versionnement prompts/modèles, tests de résilience, rétention et révocation des credentials. Utiliser des données synthétiques uniquement.

Preuves : corpus redteam RAI BFI et tests Python. Ce guide ne prétend pas déployer un service sur CRC.
