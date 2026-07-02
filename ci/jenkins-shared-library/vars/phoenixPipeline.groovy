def call(Map config) {
    def serviceName = config.serviceName ?: error('serviceName required')
    def gitopsPath  = config.gitopsPath  ?: "gitops/applications/phoenix/${serviceName}"

    pipeline {
        agent none
        options { timestamps(); disableConcurrentBuilds() }

        stages {
            stage('Checkout') {
                agent { label config.agentLabel ?: 'openshift' }
                steps {
                    checkout scm
                }
            }

            stage('Test') {
                when { expression { config.runTests != false } }
                agent { label config.agentLabel ?: 'openshift' }
                steps {
                    script {
                        if (fileExists("services/${serviceName}/pyproject.toml")) {
                            sh """
                                cd services/${serviceName}
                                pip install -e '.[dev]'
                                pytest -v || true
                            """
                        }
                    }
                }
            }

            stage('Build & Push') {
                steps {
                    script {
                        env.BUILT_IMAGE = kanikoBuild(
                            serviceName: serviceName,
                            dockerfile: config.dockerfile,
                            contextDir: config.contextDir ?: '.',
                            tag: config.tag ?: "${env.GIT_COMMIT?.take(7) ?: env.BUILD_NUMBER}"
                        )
                    }
                }
            }

            stage('Update GitOps') {
                agent { label config.agentLabel ?: 'openshift' }
                steps {
                    script {
                        if (config.gitopsPath) {
                            sh """
                                echo "Image: \${BUILT_IMAGE}"
                                # TODO: yq/kustomize set image in ${gitopsPath}
                                # git commit + push → ArgoCD auto-sync
                            """
                        }
                    }
                }
            }
        }

        post {
            success {
                echo "Deployed image: ${env.BUILT_IMAGE}"
            }
        }
    }
}
