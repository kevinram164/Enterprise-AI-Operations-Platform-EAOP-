# Platform GitOps (Helm)

ArgoCD sync **Helm charts** từ `deploy/helm/`.

## Chọn cách deploy

### Option A — Umbrella (all-in-one)

| App | Chart | Mô tả |
|-----|-------|-------|
| `phoenix-platform` | `deploy/helm/phoenix-platform` | Infra + API + Portal |

### Option B — Tách riêng (khuyến nghị)

| App | Chart |
|-----|-------|
| `phoenix-infra` | `deploy/helm/phoenix-infra` |
| `platform-api` | `deploy/helm/platform-api` |
| `admin-portal` | `deploy/helm/admin-portal` |

## Jenkins cập nhật image

Sau Kaniko push Harbor, pipeline sửa `values.yaml` hoặc `values-ocp1.npd.co.yaml`:

```yaml
platform-api:
  image:
    tag: abc1234
```

ArgoCD auto-sync.

## Legacy

`gitops/platform/overlays/` — raw YAML cũ, đã thay bằng Helm charts.
