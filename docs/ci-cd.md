# CI/CD Architecture

EAOP xây **CI/GitOps trước** — đây là paved road để build và deploy mọi service phía trên.

## Nguyên tắc

> Không build app trước khi có đường ống CI/CD + GitOps.

## Hạ tầng sẵn có

| Component | Trạng thái |
|-----------|------------|
| OpenShift (`ocp1.npd.co`) | ✅ |
| ArgoCD | ✅ |
| Vault | ✅ |
| Jenkins | ✅ |
| Harbor | ✅ |
| NFS CSI (`nfs-csi`) | ✅ |

## Stack CI/CD

```
┌─────────────┐     ┌──────────┐     ┌─────────┐     ┌───────────┐
│   Git repo  │────►│ Jenkins  │────►│ Kaniko  │────►│  Harbor   │
│   (EAOP)    │     │ + Shared │     │  build  │     │  registry │
└─────────────┘     │  Library │     └─────────┘     └─────┬─────┘
                    └────┬─────┘                           │
                         │ Vault                           │ image
                         ▼ credentials                       ▼
                    ┌──────────┐     ┌─────────┐     ┌───────────┐
                    │  Vault   │     │ GitOps  │◄────│  Update   │
                    │ secrets  │     │  repo   │     │ image tag │
                    └──────────┘     └────┬────┘     └───────────┘
                                          │
                                          ▼
                                    ┌───────────┐
                                    │  ArgoCD   │────► OpenShift
                                    └───────────┘
```

## Jenkins Shared Library

Mọi service dùng cùng pipeline pattern:

1. **Checkout** source
2. **Test** (pytest / npm test)
3. **Kaniko build** → push Harbor (`harbor.ocp1.npd.co/phoenix/<service>:<tag>`)
4. **Update GitOps** manifest image tag
5. **ArgoCD** auto-sync

Xem `ci/jenkins-shared-library/`.

## Vault secrets

| Path | Purpose |
|------|---------|
| `secret/phoenix/ci/harbor` | Registry push |
| `secret/phoenix/ci/git` | GitOps repo write |
| `secret/phoenix/ci/argocd` | Optional sync trigger |

## Harbor image naming

```
harbor.ocp1.npd.co/phoenix/<service>:<git-sha>
```

Ví dụ:
- `harbor.ocp1.npd.co/phoenix/platform-api:abc1234`
- `harbor.ocp1.npd.co/phoenix/admin-portal:abc1234`

Golden Path apps:
- `harbor.ocp1.npd.co/phoenix/<team>/<app-name>:<tag>`

## ArgoCD layout

```
gitops/
├── bootstrap/root-app.yaml
├── platform/                          # ArgoCD Apps → deploy/helm/*
│   ├── phoenix-platform.yaml          # Umbrella (all-in-one)
│   ├── phoenix-infra.yaml
│   ├── platform-api.yaml
│   └── admin-portal.yaml
└── applications/{team}/{app}/       # Golden Path apps

deploy/helm/
├── phoenix-platform/                  # Umbrella chart
├── phoenix-infra/
├── platform-api/
└── admin-portal/
```

## Roadmap (cập nhật)

| Phase | Scope | Status |
|-------|-------|--------|
| **A** | CI: Jenkins + Shared Library + Kaniko + Harbor + Vault | **Current** |
| **B** | GitOps: ArgoCD bootstrap, platform deploy | In progress |
| **C** | Golden Path → GitOps commit → ArgoCD sync apps | Planned |
| **D** | platform-api, Admin Portal, Operations services | Partial |
| **E** | AI layer (Gateway, MCP, Chat) | Planned |

## Thiết lập Jenkins job

1. **Shared Library** → trỏ repo EAOP, folder `ci/jenkins-shared-library`
2. **Pipeline job** → SCM, script path `ci/jenkinsfiles/platform-api.Jenkinsfile`
3. **Vault credential** → AppRole hoặc K8s auth
4. **Agent** → Jenkins agent pod trên OpenShift (label `openshift`)

## Bootstrap ArgoCD

```bash
oc apply -f gitops/bootstrap/root-app.yaml -n openshift-gitops
```
