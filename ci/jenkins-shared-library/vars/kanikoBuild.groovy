def call(Map config) {
    def cfg = new org.phoenix.PipelineConfig()
    def serviceName = config.serviceName ?: error('serviceName required')
    def dockerfile  = config.dockerfile  ?: "ci/docker/${serviceName}/Containerfile"
    def contextDir  = config.contextDir  ?: '.'
    def tag         = config.tag ?: env.BUILD_NUMBER ?: 'latest'
    def image       = cfg.imageRef(serviceName, tag)

    podTemplate(yaml: '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:v1.23.2
    command: ['sleep']
    args: ['infinity']
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker
  volumes:
  - name: docker-config
    emptyDir: {}
''') {
        node(POD_LABEL) {
            container('kaniko') {
                withVault(configuration: [vaultUrl: config.vaultUrl ?: 'https://vault.ocp1.npd.co',
                                            vaultCredentialId: config.vaultCredentialId ?: 'vault-approle'],
                          vaultSecrets: [[path: cfg.vaultHarborPath, secretValues: [
                              [envVar: 'HARBOR_USER', vaultKey: 'username'],
                              [envVar: 'HARBOR_PASS', vaultKey: 'password'],
                              [envVar: 'HARBOR_REGISTRY', vaultKey: 'registry']
                          ]]]) {
                    sh """
                        mkdir -p /kaniko/.docker
                        echo "{\\"auths\\":{\\"\${HARBOR_REGISTRY}\\":{\\"username\\":\\"\${HARBOR_USER}\\",\\"password\\":\\"\${HARBOR_PASS}\\"}}}" \\
                          > /kaniko/.docker/config.json
                        /kaniko/executor \\
                          --context=dir://${contextDir} \\
                          --dockerfile=${dockerfile} \\
                          --destination=${image} \\
                          --skip-tls-verify
                    """
                }
            }
        }
    }
    return image
}
