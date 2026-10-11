# D-100 M3-I3 — Kyverno Kind admission (digest-only)

**Status:** `M3_I3_DIGEST_ADMISSION_KIND_PROVEN / CRYPTO_SIGNATURE_ADMISSION_NOT_PROVEN / M3_OPEN`.

D-098 Kyverno CLI evaluations and M3-I1/I2 Syft/Grype/Cosign CI are reused. This iteration exercises the **real Kubernetes validating webhook** in a disposable Kind cluster for a digest-only image-reference requirement.

Server-side dry-run requests must prove an image containing `@sha256:` is accepted, that both `:latest` and `:1.36.1` are rejected by Kyverno policy enforcement rather than errors in parsing or networking, and that the rule is strictly scoped to namespace `d100-m3-admission`.

The test digest is intentionally synthetic. Server-side dry-run calls exercise admission but **do not pull or run an image**. Therefore the test is NOT a proof of image content or cryptographic signature verification. The separate Cosign signature denial shown in M3-I2 was a CLI/registry proof, not an admission webhook decision.

A fail-closed script requires `CI=true` and explicit `D100_M3_CI_ONLY=YES`. Unique Kind kubeconfig; unconditional cleanup. No cloud, no CRC, no secret values.

**M3 cannot be globally closed** until Kyverno admission validates trusted signed images and refuses untrusted signatures in a bounded runtime environment. OpenShift SCC admission also remains unproven.

### CI diagnostic et corrections — 11 octobre 2026

La première exécution [#38169724280](https://github.com/zdmooc/maya-secure-agentic-devsecops-platform/actions/runs/38169724280) s'est arrêtée après le lancement de Kyverno admission-controller (`Ready 1/1`) : `ClusterPolicy.status.ready` n'était pas renseigné en mode installation minimale. La seconde exécution [#38169732151](https://github.com/zdmooc/maya-secure-agentic-devsecops-platform/actions/runs/38169732151) présentait le même écart. Ce n'était **pas** un résultat d'acceptation ou de refus d'admission.

Correctif [commit `2e87a68f0b1e31a204756d4932fe7d2bf9b5cd04`](https://github.com/zdmooc/maya-secure-agentic-devsecops-platform/commit/2e87a68f0b1e31a204756d4932fe7d2bf9b5cd04) : le readiness gate sonde désormais l'API server et exige une erreur contenant **exactement le nom de la politique et le nom de la règle**. Les deux tests négatifs appliquent également ces assertions strictes pour éviter qu'une panne du webhook soit prise pour une protection effective. Exécution [#38170017755](https://github.com/zdmooc/maya-secure-agentic-devsecops-platform/actions/runs/38170017755) **en cours à la dernière vérification**. `M3_I3_RUNTIME_PENDING` jusqu'à des marqueurs de webhook positifs/négatifs et la conclusion CI SUCCESS.

## Preuve finale CI — 11 octobre 2026

- **[GitHub Actions #38170017755](https://github.com/zdmooc/maya-secure-agentic-devsecops-platform/actions/runs/38170017755) : SUCCESS**, commit `2e87a68f0b1e31a204756d4932fe7d2bf9b5cd04`. Artefact `d100-m3-kyverno-admission-kind`, ID `11713652469` (251 octets).
- Marqueurs contrôlés : `D100_M3_ADMISSION_STATIC_CONTRACT=PASS`, `D100_M3_NON_CI_GUARD=PASS`, `D100_M3_KIND_ISOLATION=PASS`, `D100_M3_KYVERNO_WEBHOOK_READY=PASS`, `D100_M3_DIGEST_ADMISSION_ACCEPT=PASS`, `D100_M3_TAG_ADMISSION_REJECT=PASS`, `D100_M3_VERSION_TAG_REJECT=PASS`, `D100_M3_POLICY_NAMESPACE_SCOPE=PASS`, `D100_M3_KYVERNO_KIND_ADMISSION_RUNTIME=PASS`.
- Il s'agit d'une **vraie décision d'admission du serveur API Kubernetes**, et non de Kyverno CLI. Les Pods ne sont pas exécutés : tous les essais utilisent un dry-run côté serveur. La valeur de digest autorisée est synthétique et n'est pas vérifiée cryptographiquement.
- **Verdict :** `M3_I1_I2_CI_VERIFIED / M3_I3_KIND_ADMISSION_DIGEST_VERIFIED / M3_GLOBAL_OPEN`. Restent : admission cryptographique vérifiant signature Cosign autorisée et refus de signature non fiable ; tests SCC/Admission spécifiques OpenShift. PR #3 en brouillon et non fusionnée.
