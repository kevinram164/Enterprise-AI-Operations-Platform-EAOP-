@Library('phoenix-shared-library') _

phoenixPipeline(
  serviceName: 'platform-api',
  dockerfile: 'ci/docker/platform-api/Containerfile',
  contextDir: '.',
  harborProject: 'phoenix',
  gitopsPath: 'deploy/helm/phoenix-platform/values-ocp1.npd.co.yaml',
  runTests: true
)
