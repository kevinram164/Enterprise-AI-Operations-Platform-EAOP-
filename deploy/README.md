# OpenShift deployment

Deploy qua **ArgoCD (GitOps)** — không dùng Docker local hay OpenShift BuildConfig.

## Hạ tầng sẵn có

| Tool | Vai trò |
|------|---------|
| OpenShift | Runtime |
| Jenkins + Kaniko | CI build |
| Harbor | Image registry |
| Vault | CI/CD credentials |
| ArgoCD | GitOps sync |

## Thứ tự triển khai

### 1. CI/CD foundation (làm trước)

Xem [ci/README.md](../../ci/README.md) và [docs/ci-cd.md](../../docs/ci-cd.md).

- Cấu hình Jenkins Shared Library
- Vault secrets (`secret/phoenix/ci/harbor`, `secret/phoenix/ci/git`)
- Jenkins pipeline → Kaniko → Harbor

### 2. Harbor pull secret trên OpenShift

```bash
oc apply -f deploy/openshift/namespaces/
oc create secret docker-registry harbor-pull-secret \
  --docker-server=harbor.ocp1.npd.co \
  --docker-username='robot$phoenix' \
  --docker-password='<from-vault>' \
  -n phoenix-platform
```

### 3. ArgoCD bootstrap

```bash
# Sửa repoURL trong gitops/bootstrap/root-app.yaml
oc apply -f gitops/bootstrap/root-app.yaml -n openshift-gitops
```

ArgoCD sync:
- `phoenix-infra` → Postgres, Redis, Redpanda
- `phoenix-infra`, `platform-api`, `admin-portal` → Helm charts trong `deploy/helm/`

### 4. Build images qua Jenkins

```bash
# Trigger Jenkins job platform-api → push harbor.ocp1.npd.co/phoenix/platform-api:<tag>
# Jenkins cập nhật image tag trong gitops/ → ArgoCD sync
```

## Manifest paths

| Manifest paths | Nội dung |
|------|----------|
| `deploy/helm/phoenix-platform/` | Umbrella chart (infra + apps) |
| `deploy/helm/phoenix-infra/` | PostgreSQL, Redis, Redpanda |
| `deploy/helm/platform-api/` | Control plane API |
| `deploy/helm/admin-portal/` | Admin UI |
| `deploy/openshift/namespaces/` | Namespace |
| `gitops/platform/` | ArgoCD Applications → Helm charts |

## Routes

| Service | URL |
|---------|-----|
| Admin Portal | https://portal.ocp1.npd.co |
| Platform API | https://api.platform.ocp1.npd.co |
