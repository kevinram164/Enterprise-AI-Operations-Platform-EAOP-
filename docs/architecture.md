# Phoenix Platform Architecture

> Repository layout: [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) · Service catalog: [services/README.md](services/README.md)

## Overview

Phoenix Platform is an Enterprise Internal Developer Platform (IDP) running on OpenShift. It provides a self-service Golden Path for developers to provision new applications with standardized infrastructure configurations.

## Design principles

1. **Cloud-native microservices** — small, independently deployable services
2. **API-first** — all capabilities exposed via REST API
3. **GitOps** — cluster state managed through Git + ArgoCD
4. **Event-driven** — Kafka for async notifications and audit trail
5. **Security-first** — RBAC, secrets management, audit logging
6. **Modular** — easy to add new templates and integrations

## High-level architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Users: Admin, Developer, Operator                          │
├─────────────────────────────────────────────────────────────┤
│  Admin Portal (Next.js)          Chat UI (Phase 3)        │
├─────────────────────────────────────────────────────────────┤
│  platform-api (FastAPI)                                     │
│    ├── Application CRUD                                     │
│    ├── Golden Path Engine                                   │
│    ├── Audit Service                                        │
│    └── Event Publisher (Kafka)                              │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL │ Redis │ Kafka/Redpanda                        │
├─────────────────────────────────────────────────────────────┤
│  GitOps Repo ──► ArgoCD ──► OpenShift (ocp1.npd.co)        │
├─────────────────────────────────────────────────────────────┤
│  AI Gateway │ MCP Server (Phase 3)                          │
└─────────────────────────────────────────────────────────────┘
```

## Core domain model

### Application

Represents a developer-owned application registered on the platform.

| Field | Description |
|-------|-------------|
| `name` | Unique slug (e.g. `payment-api`) |
| `team` | Owning team (e.g. `platform`) |
| `template` | Golden Path template (`web-api`) |
| `namespace` | Generated: `team-{team}-{name}` |
| `status` | `pending` → `provisioning` → `provisioned` |

### ProvisioningRequest

Tracks a single provisioning run and stores generated artifacts as JSON.

### AuditEvent

Immutable log of platform actions (`application.created`, `application.provisioned`, etc.).

## Golden Path

When a developer provisions an application, the engine generates:

| Artifact | Purpose |
|----------|---------|
| `namespace.yaml` | Namespace + labels |
| `resourcequota.yaml` | CPU/memory limits per app |
| `helm-values.yaml` | Application deployment config |
| `argocd-application.yaml` | ArgoCD sync target |
| `route.yaml` | OpenShift Route (`{app}.apps.ocp1.npd.co`) |
| `keycloak-client.json` | OIDC client stub |
| `postgres-config.yaml` | Database connection ref |
| `redis-config.yaml` | Cache connection ref |
| `kafka-topic.yaml` | Event topic config |
| `otel-config.yaml` | OpenTelemetry exporter |
| `servicemonitor.yaml` | Prometheus scrape config |

Templates live in `templates/golden-path/{template}/` using Jinja2.

## Target OpenShift cluster

| Resource | Specification |
|----------|---------------|
| Control plane | 3 × 4 vCPU, 16 GB RAM, 120 GB disk |
| Workers | 3 × 4 vCPU, 16 GB RAM, 120 GB disk |
| DNS | `ocp1.npd.co` |
| Storage | NFS CSI (`nfs-csi`), 200 GB |
| GitOps | ArgoCD (pre-installed) |

### Namespace layout

```
phoenix-platform          # Platform services (api, portal, PG, Redis, Kafka)
team-{team}-{app}         # Per-application namespace (Golden Path)
openshift-gitops          # ArgoCD (existing)
```

### Resource budget (platform stack)

| Service | CPU request | Memory request | PVC |
|---------|-------------|----------------|-----|
| platform-api | 200m | 256Mi | — |
| admin-portal | 100m | 128Mi | — |
| PostgreSQL | 250m | 512Mi | 10–20 GB |
| Redis | 100m | 128Mi | 1 GB |
| Redpanda/Kafka | 500m | 512Mi | 20–30 GB |

## API design

Base path: `/api/v1`

| Method | Endpoint | Phase | Description |
|--------|----------|-------|-------------|
| `GET` | `/health` | 0 | Health check |
| `POST` | `/applications` | 0 | Register new application |
| `GET` | `/applications` | 0 | List applications |
| `GET` | `/applications/{id}` | 0 | Get application details |
| `POST` | `/applications/{id}/provision` | 1 | Run Golden Path |
| `GET` | `/applications/{id}/artifacts` | 1 | View generated manifests |
| `GET` | `/audit` | 1 | Query audit log |

## Event topics (Kafka)

| Topic | Payload |
|-------|---------|
| `phoenix.application.created` | Application registered |
| `phoenix.application.provisioned` | Golden Path completed |
| `phoenix.application.failed` | Provisioning error |

## Development phases

| Phase | Deliverables | Status |
|-------|-------------|--------|
| 0 | Monorepo, platform-api, OpenShift manifests, docs | Done |
| 1 | Golden Path engine, provision API, admin portal | **Current** |
| 2 | GitOps repo, ArgoCD sync, Helm on OpenShift | Planned |
| 3 | AI Gateway, MCP skeleton, OpenTelemetry | Planned |

## Security (MVP → Production)

| Concern | MVP | Production |
|---------|-----|------------|
| Authentication | API open / API key | Keycloak OIDC |
| Authorization | Team label on resources | RBAC + OPA |
| Secrets | K8s Secrets / stubs | Vault + ESO |
| TLS | OpenShift edge termination | mTLS internal |
| Audit | PostgreSQL audit_events | + SIEM export |
