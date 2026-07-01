# Platform API

**Path:** `services/platform-api/`  
**Status:** active  
**Stack:** Python 3.12, FastAPI, SQLAlchemy, Alembic

## Role

Control plane and orchestrator for the Enterprise Platform:

- Application registry (self-service IDP)
- Golden Path provisioning engine
- Audit events (MVP — migrate to audit-service later)
- Kafka event publishing

## API

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/applications` | Register app |
| `POST /api/v1/applications/{id}/provision` | Run Golden Path |
| `GET /api/v1/applications/{id}/artifacts` | Get manifests |
| `GET /api/v1/audit` | Audit log |

## Dependencies

PostgreSQL, Redis, Kafka on OpenShift (`phoenix-platform` namespace). See `deploy/openshift/`.
