# Phoenix Platform Umbrella Chart

Deploy toàn bộ platform stack lên `phoenix-platform` namespace.

```bash
cd deploy/helm/phoenix-platform
helm dependency update
helm upgrade --install phoenix . \
  -f values.yaml \
  -f values-ocp1.npd.co.yaml \
  -n phoenix-platform --create-namespace
```

ArgoCD sync chart này — xem `gitops/platform/phoenix-platform.yaml`.
