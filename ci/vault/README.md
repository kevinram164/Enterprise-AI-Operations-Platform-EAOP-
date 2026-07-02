# Vault — CI/CD secrets

Jenkins lấy credentials từ Vault (KV v2). Không lưu secret trong Git.

## Paths (convention)

| Path | Keys | Dùng cho |
|------|------|----------|
| `secret/phoenix/ci/harbor` | `username`, `password`, `registry` | Kaniko push Harbor |
| `secret/phoenix/ci/git` | `username`, `password` | Clone/push GitOps repo |
| `secret/phoenix/ci/argocd` | `token` | Trigger sync (optional) |

## Ví dụ tạo secret

```bash
vault kv put secret/phoenix/ci/harbor \
  registry=harbor.ocp1.npd.co \
  username=robot$phoenix \
  password='<harbor-robot-token>'
```

## Jenkins integration

Dùng **HashiCorp Vault Plugin** hoặc **Kubernetes auth** từ Jenkins pod trên OpenShift.

Shared library gọi `withVault` để inject credentials vào Kaniko stage.
