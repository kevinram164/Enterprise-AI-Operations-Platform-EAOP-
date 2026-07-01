# Kong API Gateway

Kong route definitions, plugins, and upstream configs.

**Type:** vendor + config  
**Status:** planned  
**Deploy:** `deploy/helm/kong/`

## Responsibilities

- Central API routing for all platform services
- Authentication plugins (OIDC via Keycloak)
- Rate limiting, request/response logging

## Repo contents

- `routes/` — per-service route YAML
- `plugins/` — shared plugin configs

See [docs/services/api-gateway.md](../../docs/services/api-gateway.md)
