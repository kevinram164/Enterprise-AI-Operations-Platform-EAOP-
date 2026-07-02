# Enterprise AI Operations Platform — Repository Structure

```
enterprise-ai-operations-platform/
│
├── apps/                              # Frontend applications
│   ├── admin-portal/                  # Self-service IDP UI (active)
│   ├── dashboard/                     # Operations dashboard (planned)
│   └── chat-ui/                       # AI assistant chat (planned)
│
├── services/                          # Backend microservices
│   ├── platform-api/                  # Control plane + Golden Path (active)
│   ├── core/
│   │   ├── iam-service/               # Keycloak wrapper API
│   │   ├── audit-service/             # Audit log service
│   │   └── notification-service/    # Email, Teams, Slack, webhook
│   ├── operations/
│   │   ├── cmdb-service/
│   │   ├── ticket-service/
│   │   ├── workflow-service/
│   │   ├── asset-service/
│   │   └── cost-service/
│   ├── infrastructure/
│   │   ├── k8s-manager/               # OpenShift/Kubernetes API
│   │   └── cloud-manager/             # VMware / cloud resources
│   ├── ai/
│   │   ├── ai-gateway/                # LLM proxy + guardrails
│   │   ├── ai-agent/                  # NLP + action execution
│   │   ├── mcp-server/                # Model Context Protocol tools
│   │   └── knowledge-service/         # RAG + vector store
│   └── observability/
│       ├── monitoring-service/        # Metrics aggregation API
│       └── logging-service/           # Log query API
│
├── gateways/                          # Gateway configs (not app logic)
│   └── kong/                          # Kong routes, plugins
│
├── ci/                                # Jenkins Shared Library + Kaniko
│   ├── jenkins-shared-library/
│   ├── jenkinsfiles/
│   ├── docker/                        # Containerfiles
│   └── vault/                         # Vault path conventions
│
├── deploy/                            # OpenShift infra manifests
│   │   ├── phoenix-platform/          # Umbrella chart
│   │   ├── keycloak/
│   │   ├── kong/
│   │   ├── otel-collector/
│   │   └── instana-agent/
│   └── openshift/
│       ├── namespaces/
│       └── storageclasses/            # nfs-csi notes
│
├── gitops/                            # ArgoCD manifests
│   ├── bootstrap/                     # App of Apps root
│   ├── platform/                      # Platform stack apps
│   └── applications/                  # Golden Path app output
│
├── templates/
│   └── golden-path/                   # Jinja2 provisioning templates
│
├── docs/
│   ├── architecture.md
│   ├── REPOSITORY_STRUCTURE.md        # This file
│   └── services/                      # Per-service specifications
│
└── .github/workflows/
```

## Service status legend

| Status | Meaning |
|--------|---------|
| **active** | Code implemented, in development |
| **planned** | Spec + skeleton only |
| **vendor** | Deployed via Helm, minimal custom code |

## Layer responsibilities

| Layer | Role |
|-------|------|
| `apps/` | User-facing UI |
| `services/platform-api` | Orchestrator, Golden Path, app registry |
| `services/core` | Identity, audit, notifications |
| `services/operations` | ITSM + CMDB + workflow |
| `services/infrastructure` | Cluster and cloud management |
| `services/ai` | AI capabilities |
| `services/observability` | Monitoring and logging APIs |
| `gateways/` | Kong route definitions |
| `deploy/` | Helm charts, OpenShift manifests, cluster builds |
| `gitops/` | ArgoCD sync targets |
