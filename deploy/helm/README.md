# Helm Charts

Helm là **cách deploy chuẩn** cho EAOP — ArgoCD sync Helm charts, Jenkins cập nhật `image.tag` trong values.

## Charts

| Chart | Path | Mô tả |
|-------|------|-------|
| **phoenix-platform** | `phoenix-platform/` | Umbrella — deploy toàn bộ stack |
| **phoenix-infra** | `phoenix-infra/` | PostgreSQL, Redis, Redpanda |
| **platform-api** | `platform-api/` | Control plane API |
| **admin-portal** | `admin-portal/` | Admin UI |
| keycloak | `keycloak/` | Planned (vendor chart) |
| kong | `kong/` | Planned (vendor chart) |
| otel-collector | `otel-collector/` | Planned |
| instana-agent | `instana-agent/` | Planned |

## Cấu trúc

```
deploy/helm/
├── phoenix-platform/          # Umbrella chart
│   ├── Chart.yaml             # dependencies
│   ├── values.yaml
│   └── values-ocp1.npd.co.yaml
├── phoenix-infra/
├── platform-api/
└── admin-portal/
```

## Local render (không cần cluster)

```bash
cd deploy/helm/phoenix-platform
helm dependency update
helm template phoenix . -f values.yaml -f values-ocp1.npd.co.yaml -n phoenix-platform
```

## ArgoCD

ArgoCD Application trỏ tới chart + values:

```yaml
source:
  path: deploy/helm/phoenix-platform
  helm:
    valueFiles:
      - values.yaml
      - values-ocp1.npd.co.yaml
```

## Jenkins → Helm

Pipeline cập nhật image tag sau Kaniko build:

```bash
# yq -i '.platform-api.image.tag = strenv(GIT_SHA)' values-ocp1.npd.co.yaml
git commit + push → ArgoCD sync
```

## Golden Path apps

Template `web-api` sinh `helm-values.yaml` — mỗi app team dùng chart riêng hoặc generic `app` chart (Phase C).
