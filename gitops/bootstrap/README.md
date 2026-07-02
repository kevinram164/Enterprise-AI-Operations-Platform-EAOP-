# GitOps Bootstrap

ArgoCD App of Apps — entry point cho toàn bộ EAOP.

## Apply

```bash
# 1. Sửa repoURL trong root-app.yaml
# 2. Apply
oc apply -f gitops/bootstrap/root-app.yaml -n openshift-gitops
```

`eaop-root` sync folder `gitops/platform/` gồm:
- `phoenix-infra` — data layer
- `platform-api` — control plane
- `admin-portal` — UI

## Prerequisites

- ArgoCD running in `openshift-gitops`
- Jenkins đã build & push image lên Harbor
- `harbor-pull-secret` trong `phoenix-platform` namespace
