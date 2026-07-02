# Jenkins Shared Library

Load trong Jenkinsfile:

```groovy
@Library('phoenix-shared-library') _
phoenixPipeline(
  serviceName: 'platform-api',
  dockerfile: 'ci/docker/platform-api/Containerfile',
  contextDir: '.',
  harborProject: 'phoenix',
  gitopsPath: 'gitops/platform/overlays/platform-api'
)
```

## Cấu trúc

```
jenkins-shared-library/
├── vars/
│   ├── phoenixPipeline.groovy    # Entry — full CI pipeline
│   └── kanikoBuild.groovy        # Kaniko build + push Harbor
└── src/org/phoenix/
    └── PipelineConfig.groovy     # Defaults & validation
```

## Cài đặt trên Jenkins

**Manage Jenkins → System → Global Pipeline Libraries**

| Field | Value |
|-------|-------|
| Name | `phoenix-shared-library` |
| Default version | `main` |
| Retrieval | Modern SCM → Git → URL repo EAOP |
