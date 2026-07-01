# Phoenix Platform on OpenShift

Namespace: `phoenix-platform`  
Cluster: `ocp1.npd.co`

## Order of apply

```bash
oc apply -f deploy/openshift/namespaces/
oc apply -f deploy/openshift/phoenix-platform/infra/
oc apply -f deploy/openshift/phoenix-platform/builds/

# From repo root — builds run ON the cluster (no local Docker)
oc start-build platform-api --from-dir=. --wait -n phoenix-platform
oc start-build admin-portal --from-dir=. --wait -n phoenix-platform

oc apply -f deploy/openshift/phoenix-platform/apps/
```

## Before production

1. Change `postgres-credentials` and `platform-api-secret` passwords
2. Confirm StorageClass `nfs-csi` exists (`oc get sc nfs-csi`)
3. Point DNS `portal.ocp1.npd.co` and `api.platform.ocp1.npd.co` to OpenShift router

## Routes

| Host | Service |
|------|---------|
| `portal.ocp1.npd.co` | admin-portal |
| `api.platform.ocp1.npd.co` | platform-api |
