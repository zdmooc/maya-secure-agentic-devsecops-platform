# D-100 M3 I1 — Syft, Grype et Checkov

**État : CODE_COMMITTED_PR_DRAFT / CI_PENDING / M3_NOT_CLOSED.** Aucune mutation CRC ou cloud.

## Réutilisation

La preuve D-098 existante est **CI_PROVEN** : Trivy scan, digest OCI, Cosign sign/verify et refus d'une clé non fiable, Kyverno CLI autorisé/refusé : [run 37517552045](https://github.com/zdmooc/maya-secure-agentic-devsecops-platform/actions/runs/37517552045). Ne pas redévelopper.

## Extension sous test

- `anchore/sbom-action@v0.24.0` produit un SBOM SPDX JSON pour une image jetable `proofs/d098`.
- `anchore/scan-action@v7` exécute Grype sur le SBOM ; `fail-build=true`, `severity-cutoff=high`. Rapport JSON conservé.
- `bridgecrew/checkov:3.3.20` (CLI Docker) vérifie Dockerfile : `CKV_DOCKER_2` HEALTHCHECK et `CKV_DOCKER_3` USER. La fixture conforme doit réussir, l'invalide doit échouer **sur les deux check_ids**. La version action testée initialement ignorait le paramètre `file` et balayait tout le dépôt (CI échec); le CLI isolé corrige précisément ce problème. Les résultats JSON sont lus pour confirmer le refus.
- GitHub Actions token `contents: read` ; pas de secrets ni accès à un vrai registre. Artifacts retenus 14 jours. Aucun workload modifié.

## Vérité des preuves

Le conteneur témoin est `FROM scratch`, sans dépendances OS significatives. Une analyse Grype ne trouvant aucune CVE **ne prouve pas encore le rejet effectif de CVE HIGH**. Une seconde itération devra prouver ce rejet sur fixture sûre et contrôlée.

Checkov CI n'est PAS une admission réelle Kyverno sur OpenShift. Les mesures actuelles ne ferment pas M3, ni M1/M2/M4/M5/M6. Une preuve de réussite du workflow sous un SHA précis reste obligatoire.

## Conditions de promotion

- [ ] PR GitHub Actions verte sur les deux jobs
- [ ] SBOM SPDX JSON valide
- [ ] Grype JSON produit et gate HIGH configuré
- [ ] Checkov good 2/2 PASS, bad 2/2 FAIL, assertions PASS
- [ ] Artefacts présents avec SHA/run
- [ ] Grype HIGH-CVE negative proof sur fixture représentative (iteration suivante)
- [ ] Admission runtime testée réellement sous Kubernetes/OpenShift (autre itération après préflight)
