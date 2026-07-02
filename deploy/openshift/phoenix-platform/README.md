# Phoenix Platform on OpenShift

Deploy qua **Jenkins → Harbor → ArgoCD**. Không dùng OpenShift BuildConfig.

## Bootstrap

```bash
# 1. Namespace + Harbor pull secret
oc apply -f deploy/openshift/namespaces/
# xem harbor-pull-secret.md

# 2. ArgoCD
oc apply -f gitops/bootstrap/root-app.yaml -n openshift-gitops

# 3. Jenkins build platform-api + admin-portal → Harbor
# 4. ArgoCD sync apps tự động
```

## Infra only (manual nếu cần)

```bash
oc apply -f deploy/openshift/phoenix-platform/infra/
```

## Storage

PVC dùng `storageClassName: nfs-csi`
