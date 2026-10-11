# D-100 M3 I1 — Syft, Grype et Checkov

**État : CI_VERIFIED_BOUND_M3_I1 / PR_DRAFT / M3_NOT_CLOSED.** Aucune mutation CRC ou cloud.

## Réutilisation

La preuve D-098 existante est **CI_PROVEN** : Trivy scan, digest OCI, Cosign sign/verify et refus d'une clé non fiable, Kyverno CLI autorisé/refusé : [run 37517552045](https://github.com/zdmooc/maya-secure-agentic-devsecops-platform/actions/runs/37517552045). Ne pas redévelopper.

## Extension sous test

- `anchore/sbom-action@v0.24.0` produit un SBOM SPDX JSON pour une image jetable `proofs/d098`.
- `anchore/scan-action@v7` exécute Grype sur le SBOM ; `fail-build=true`, `severity-cutoff=high`. Rapport JSON conservé.
- `bridgecrew/checkov:3.3.20` (CLI Docker) vérifie Dockerfile : `CKV_DOCKER_2` HEALTHCHECK et `CKV_DOCKER_3` USER. La fixture conforme doit réussir, l'invalide doit échouer **sur les deux check_ids**. La version action testée initialement ignorait le paramètre `file` et balayait tout le dépôt (CI échec); le CLI isolé corrige précisément ce problème. Les résultats JSON sont lus pour confirmer le refus.
- GitHub Actions token `contents: read` ; pas de secrets ni accès à un vrai registre. Artifacts retenus 14 jours. Aucun workload modifié.

## Vérité des preuves

Le conteneur témoin est `FROM scratch`, sans dépendances OS significatives. Une analyse Grype ne trouvant aucune CVE **ne prouve pas encore le rejet effectif de CVE HIGH**. Une seconde itération devra prouver ce rejet sur fixture sûre et contrôlée.

Checkov CI n'est PAS une admission réelle Kyverno sur OpenShift. Les mesures actuelles ne ferment pas M3, ni M1/M2/M4/M5/M6. Preuve CI vérifiée ci-dessous ; une promotion globale M3 exige en plus un rejet Grype HIGH sur un composant vulnérable représentatif et l'admission cluster réelle.

## Conditions de promotion

- [ ] PR GitHub Actions verte sur les deux jobs
- [ ] SBOM SPDX JSON valide
- [ ] Grype JSON produit et gate HIGH configuré
- [ ] Checkov good 2/2 PASS, bad 2/2 FAIL, assertions PASS
- [ ] Artefacts présents avec SHA/run
- [ ] Grype HIGH-CVE negative proof sur fixture représentative (iteration suivante)
- [ ] Admission runtime testée réellement sous Kubernetes/OpenShift (autre itération après préflight)

## Preuve CI du 11 octobre 2026

- **Workflow run :** [38144957583](https://github.com/zdmooc/maya-secure-agentic-devsecops-platform/actions/runs/38144957583), évènement `pull_request`, **SUCCESS**.
- **Commit exécuté :** `b33bbae9841d155d2fee21d8a16cbae900eed90c` (code workflow et deux Dockerfiles).
- **Job syft-grype :** `SUCCESS`, marqueurs `D100_M3_SBOM_VALID=PASS` et `D100_M3_GRYPE_REPORT=PASS` dans les logs, artefact `d100-m3-sbom-grype` (GitHub ID `11703664883`, 2 927 octets).
- **Job checkov :** `SUCCESS`, marqueurs `D100_M3_CHECKOV_PASS=PASS` et `D100_M3_CHECKOV_REJECTION=PASS`, artefact `d100-m3-checkov` (GitHub ID `11703554075`, 2 126 octets).
- **Correction technique observée :** l'action `bridgecrewio/checkov-action@v12.1347.0` ignorait l'entrée `file` et scannait `.` avec son conteneur Checkov 2.0.930. Remplacée par `bridgecrew/checkov:3.3.20` appelé explicitement sur chaque fixture. Un flag CLI non supporté a été retiré. Les deux jobs ont finalement été observés verts sous le commit ci-dessus.
- **Limites :** image `FROM scratch`, zéro CVE ne vaut pas test négatif de blocage d'une CVE HIGH ; `Kyverno CLI` D-098 ne vaut pas admission webhook OpenShift. Le registre et la signature sur une chaîne de promotion réelle ne sont pas testés dans cette itération.

**Décision :** sous-gate `M3_I1_CI_VERIFIED` ; **D-100 M3 demeure OPEN**. Garder la PR #3 en brouillon jusqu'à revue ; le chantier suivant est l'extension Grype négative et l'intégration M2 selon signal mission.
