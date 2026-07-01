# OpenShift deployment

All components deploy to cluster `ocp1.npd.co`. No local Docker required.

## Prerequisites

- `oc` CLI logged in to OpenShift
- StorageClass `nfs-csi` available on cluster (see `openshift/storageclasses/`)
- ArgoCD installed (for GitOps phase)

## Deploy platform stack

```bash
# 1. Namespace + storage
oc apply -f deploy/openshift/namespaces/

# 2. Data layer (PostgreSQL, Redis, Redpanda)
oc apply -f deploy/openshift/phoenix-platform/infra/

# 3. Build images on cluster (no local Docker)
oc apply -f deploy/openshift/phoenix-platform/builds/
oc start-build platform-api --from-dir=. --wait
oc start-build admin-portal --from-dir=. --wait

# 4. Platform services
oc apply -f deploy/openshift/phoenix-platform/apps/
```

## Routes (default)

| Service | Route |
|---------|-------|
| platform-api | `api.platform.ocp1.npd.co` |
| admin-portal | `portal.ocp1.npd.co` |

## Configure

Copy and edit secrets before applying apps:

```bash
cp deploy/openshift/phoenix-platform/config.env.example .env
# Edit values, then create secret:
oc create secret generic platform-api-config \
  --from-env-file=.env \
  -n phoenix-platform --dry-run=client -o yaml | oc apply -f -
```

## GitOps (Phase 2)

Platform and Golden Path apps sync via ArgoCD — see `gitops/`.
