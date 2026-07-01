# Enterprise AI Operations Platform (EAOP)

Enterprise Internal Developer Platform — deploy **only on OpenShift** (`ocp1.npd.co`).

## Repository layout

```
apps/                    # Admin Portal, Dashboard, Chat UI
services/platform-api/   # Control plane + Golden Path (active)
deploy/openshift/        # Manifests, BuildConfigs (no local Docker)
gitops/                  # ArgoCD manifests
templates/golden-path/   # Provisioning templates
docs/                    # Architecture + service specs
```

Full tree: [docs/REPOSITORY_STRUCTURE.md](docs/REPOSITORY_STRUCTURE.md)

## Deploy on OpenShift

See [deploy/README.md](deploy/README.md) for full guide.

```bash
oc login --token=... --server=https://api.ocp1.npd.co:6443

# Namespace + infra
oc apply -f deploy/openshift/namespaces/
oc apply -f deploy/openshift/phoenix-platform/infra/

# Build on cluster (binary build — no local Docker)
oc apply -f deploy/openshift/phoenix-platform/builds/
oc start-build platform-api --from-dir=. --wait -n phoenix-platform
oc start-build admin-portal --from-dir=. --wait -n phoenix-platform

# Deploy apps
oc apply -f deploy/openshift/phoenix-platform/apps/
```

## Routes

| Service | URL |
|---------|-----|
| Admin Portal | https://portal.ocp1.npd.co |
| Platform API | https://api.platform.ocp1.npd.co |
| API docs | https://api.platform.ocp1.npd.co/docs |

## Service catalog

[docs/services/](docs/services/)

## License

MIT — see [LICENSE](LICENSE).
