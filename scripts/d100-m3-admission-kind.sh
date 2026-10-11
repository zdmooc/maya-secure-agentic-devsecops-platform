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
test "$(kubectl get clusterpolicy d100-m3-require-digest -o jsonpath='{.spec.rules[0].name}')" = require-image-digest
# A policy can lack status.ready when ancillary controllers are disabled.
# Probe the actual Kubernetes admission webhook instead of waiting for status.
READY=no
for attempt in $(seq 1 50); do
  if kubectl create -f "$ROOT/proofs/d100/admission/bad-pod.yaml" \
      --dry-run=server -o name > "$WORK/probe.out" 2> "$WORK/probe.err"; then
    sleep 2
    continue
  fi
  if grep -q 'd100-m3-require-digest' "$WORK/probe.err" &&
      grep -q 'require-image-digest' "$WORK/probe.err"; then
    READY=yes
    break
  fi
  sleep 2
done
[ "$READY" = yes ]
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
grep -q 'd100-m3-require-digest' "$WORK/rejected.err"
grep -q 'require-image-digest' "$WORK/rejected.err"
echo D100_M3_TAG_ADMISSION_REJECT=PASS

sed 's/:latest/:1.36.1/' "$ROOT/proofs/d100/admission/bad-pod.yaml" \
  > "$WORK/nonlatest.yaml"
if kubectl create -f "$WORK/nonlatest.yaml" --dry-run=server \
   > "$WORK/rejected2.out" 2> "$WORK/rejected2.err"; then
  echo D100_M3_VERSION_TAG_REJECT=FAIL
  exit 1
fi
grep -q 'd100-m3-require-digest' "$WORK/rejected2.err"
grep -q 'require-image-digest' "$WORK/rejected2.err"
echo D100_M3_VERSION_TAG_REJECT=PASS

sed 's/namespace: d100-m3-admission/namespace: default/' \
  "$ROOT/proofs/d100/admission/bad-pod.yaml" > "$WORK/unscoped.yaml"
kubectl create -f "$WORK/unscoped.yaml" --dry-run=server -o name \
  > "$WORK/unscoped.out"
grep -q '^pod/d100-m3-refused' "$WORK/unscoped.out"
echo D100_M3_POLICY_NAMESPACE_SCOPE=PASS
echo D100_M3_KYVERNO_KIND_ADMISSION_RUNTIME=PASS

# Separate cryptographic gate: public fixture signed by Kyverno's documented
# demo public key. Previous digest-only policy would block the image tags,
# therefore remove it before running verifyImages admission.
kubectl delete clusterpolicy d100-m3-require-digest --wait=true >/dev/null
kubectl apply -f "$ROOT/proofs/d100/admission/signature-policy.yaml" >/dev/null
test "$(kubectl get clusterpolicy d100-m3-cosign-signature \
  -o jsonpath='{.spec.rules[0].name}')" = verify-image-signature

write_fixture() {
  local name="$1" reference="$2" outfile="$3"
  cat > "$outfile" <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: $name
  namespace: d100-m3-admission
spec:
  containers:
    - name: fixture
      image: "$reference"
      command: ["sleep", "3600"]
EOF
}
write_fixture d100-m3-crypto-accepted \
  ghcr.io/kyverno/test-verify-image:signed "$WORK/signed.yaml"
write_fixture d100-m3-crypto-unsigned \
  ghcr.io/kyverno/test-verify-image:unsigned "$WORK/unsigned.yaml"
write_fixture d100-m3-crypto-other-signer \
  ghcr.io/kyverno/test-verify-image:signed-by-someone-else "$WORK/other.yaml"

# On a real policy failure only the expected policy/rule must explain denial.
# A registry timeout, webhook error or image lookup problem MUST fail the test.
SIGNED_READY=no
for i in $(seq 1 12); do
  if kubectl create -f "$WORK/signed.yaml" --dry-run=server -o name \
      > "$WORK/signed.out" 2> "$WORK/signed.err"; then
    if grep -q '^pod/d100-m3-crypto-accepted' "$WORK/signed.out"; then
      SIGNED_READY=yes; break
    fi
  fi
  sleep 3
done
if [ "$SIGNED_READY" != yes ]; then
  echo "D100_M3_CRYPTO_ACCEPT_NOT_PROVEN=FAIL"
  sed -E 's#(https?://)[^ ]+#\1<redacted>#g' "$WORK/signed.err" | tail -8 >&2 || true
  exit 1
fi
echo D100_M3_SIGNED_IMAGE_ADMISSION_ACCEPT=PASS

for variant in unsigned other; do
  if kubectl create -f "$WORK/$variant.yaml" --dry-run=server -o name \
      > "$WORK/$variant.out" 2> "$WORK/$variant.err"; then
    echo "D100_M3_CRYPTO_$variant_DENIAL_FAILED" >&2; exit 1
  fi
  grep -q 'd100-m3-cosign-signature' "$WORK/$variant.err"
  grep -q 'verify-image-signature' "$WORK/$variant.err"
  # Require a verification/signer reason; missing registry connectivity is
  # not proof of a cryptographic authorization failure.
  grep -Eiq 'signature not found|invalid signature|no matching signatures|signature verification failed' \
    "$WORK/$variant.err"
done
echo D100_M3_UNSIGNED_IMAGE_ADMISSION_REJECT=PASS
echo D100_M3_DIFFERENT_SIGNER_ADMISSION_REJECT=PASS
echo D100_M3_COSIGN_CRYPTO_KYVERNO_ADMISSION_RUNTIME=PASS
echo "LIMIT: vendor demo fixture on Kind; no OpenShift SCC or enterprise registry PKI"
echo "LIMIT: Digest syntax gate only; Cosign signature and OpenShift SCC not proven"
