#!/usr/bin/env bash
# D100 M3-I3: real Kyverno admission on disposable Kind; NEVER user CRC.
set -euo pipefail
if [ "$CI" != true ] || [ "$D100_M3_CI_ONLY" != YES ]; then
  echo "D100_M3_REFUSED_NON_CI" >&2
  exit 2
fi
for x in docker kind kubectl helm openssl; do
  command -v "$x" >/dev/null || { echo "Missing $x" >&2; exit 2; }
done
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLUSTER="d100-m3-$(openssl rand -hex 4)"
WORK="$(mktemp -d)"
export KUBECONFIG="$WORK/kubeconfig"
NS=d100-m3-admission

cleanup() {
  status=$?
  trap - EXIT
  if [ "$status" -ne 0 ]; then
    echo "D100_M3_FAILURE_STATUS_ONLY"
    kubectl -n kyverno get deploy,pods 2>/dev/null || true
    kubectl get clusterpolicy d100-m3-require-digest \
      -o 'custom-columns=NAME:.metadata.name,READY:.status.ready' 2>/dev/null || true
  fi
  kind delete cluster --name "$CLUSTER" >/dev/null 2>&1 || true
  rm -rf "$WORK"
  exit "$status"
}
trap cleanup EXIT

kind create cluster --name "$CLUSTER" --image kindest/node:v1.31.0 --wait 140s
test "$(kubectl config current-context)" = "kind-$CLUSTER"
kubectl create namespace "$NS"
echo D100_M3_KIND_ISOLATION=PASS

helm repo add kyverno https://kyverno.github.io/kyverno/ >/dev/null
helm repo update >/dev/null
helm install kyverno kyverno/kyverno --version 3.5.2 \
  -n kyverno --create-namespace --wait --timeout 8m \
  --set backgroundController.enabled=false \
  --set cleanupController.enabled=false \
  --set reportsController.enabled=false >/dev/null
kubectl -n kyverno rollout status deploy/kyverno-admission-controller --timeout=180s
kubectl apply -f "$ROOT/proofs/d100/admission/policy.yaml" >/dev/null
kubectl wait clusterpolicy d100-m3-require-digest \
  --for=jsonpath='{.status.ready}'=true --timeout=120s
echo D100_M3_KYVERNO_WEBHOOK_READY=PASS

# Actual API server-side dry run: webhook executes, but no image is pulled.
kubectl create -f "$ROOT/proofs/d100/admission/good-pod.yaml" \
  --dry-run=server -o name > "$WORK/positive.out"
grep -q '^pod/d100-m3-accepted' "$WORK/positive.out"
echo D100_M3_DIGEST_ADMISSION_ACCEPT=PASS

if kubectl create -f "$ROOT/proofs/d100/admission/bad-pod.yaml" \
  --dry-run=server -o name > "$WORK/rejected.out" 2> "$WORK/rejected.err"; then
  echo D100_M3_TAG_ADMISSION_REJECT=FAIL
  exit 1
fi
grep -Eiq 'kyverno|d100-m3-require-digest|require-image-digest' "$WORK/rejected.err"
echo D100_M3_TAG_ADMISSION_REJECT=PASS

sed 's/:latest/:1.36.1/' "$ROOT/proofs/d100/admission/bad-pod.yaml" \
  > "$WORK/nonlatest.yaml"
if kubectl create -f "$WORK/nonlatest.yaml" --dry-run=server \
   > "$WORK/rejected2.out" 2> "$WORK/rejected2.err"; then
  echo D100_M3_VERSION_TAG_REJECT=FAIL
  exit 1
fi
grep -Eiq 'kyverno|d100-m3-require-digest|require-image-digest' "$WORK/rejected2.err"
echo D100_M3_VERSION_TAG_REJECT=PASS

sed 's/namespace: d100-m3-admission/namespace: default/' \
  "$ROOT/proofs/d100/admission/bad-pod.yaml" > "$WORK/unscoped.yaml"
kubectl create -f "$WORK/unscoped.yaml" --dry-run=server -o name \
  > "$WORK/unscoped.out"
grep -q '^pod/d100-m3-refused' "$WORK/unscoped.out"
echo D100_M3_POLICY_NAMESPACE_SCOPE=PASS
echo D100_M3_KYVERNO_KIND_ADMISSION_RUNTIME=PASS
echo "LIMIT: Digest syntax gate only; Cosign signature and OpenShift SCC not proven"
