# CI/CD — Jenkins + Kaniko + Harbor + Vault

EAOP dùng **CI/GitOps làm nền tảng** — build và deploy mọi layer phía trên.

## Stack (đã có sẵn trên cluster)

| Tool | Vai trò |
|------|---------|
| **Jenkins** | CI orchestration |
| **Jenkins Shared Library** | Pipeline chuẩn hóa cho mọi service |
| **Kaniko** | Build image không cần Docker daemon |
| **Harbor** | Container registry |
| **Vault** | Credentials cho CI/CD (Harbor, Git, ArgoCD) |
| **ArgoCD** | GitOps continuous delivery |

## Luồng

```
Git push → Jenkins (Shared Library)
              ├── Vault: lấy Harbor/Git credentials
              ├── Kaniko: build image → push Harbor
              └── Cập nhật image tag trong gitops/
                        ↓
                   ArgoCD sync → OpenShift
```

## Cấu trúc

```
ci/
├── jenkins-shared-library/   # Shared library (@Library)
├── jenkinsfiles/             # Pipeline per service
├── docker/                   # Containerfile cho Kaniko
└── vault/                    # Vault path conventions
```

## Quick start

1. Cấu hình Jenkins Shared Library trỏ tới `ci/jenkins-shared-library`
2. Lưu credentials trong Vault (xem `ci/vault/README.md`)
3. Tạo Jenkins job multibranch hoặc pipeline từ `ci/jenkinsfiles/platform-api.Jenkinsfile`
4. Bootstrap ArgoCD: `oc apply -f gitops/bootstrap/`

Chi tiết: [docs/ci-cd.md](../docs/ci-cd.md)
