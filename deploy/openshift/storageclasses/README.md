# Storage — NFS CSI

Cluster uses StorageClass **`nfs-csi`** (NFS CSI driver, 200 GB export).

## Verify

```bash
oc get storageclass nfs-csi
```

All PVCs in this repo reference `storageClassName: nfs-csi` — no extra StorageClass manifest needed.

## Current usage

| PVC | Namespace | Size | Purpose |
|-----|-----------|------|---------|
| `postgres-data` | `phoenix-platform` | 10Gi | Platform PostgreSQL |

Adjust sizes in `deploy/openshift/phoenix-platform/infra/` if needed.
