@Library('phoenix-shared-library') _

phoenixPipeline(
  serviceName: 'admin-portal',
  dockerfile: 'ci/docker/admin-portal/Containerfile',
  contextDir: '.',
  harborProject: 'phoenix',
  gitopsPath: 'deploy/helm/phoenix-platform/values-ocp1.npd.co.yaml',
  runTests: false
)
