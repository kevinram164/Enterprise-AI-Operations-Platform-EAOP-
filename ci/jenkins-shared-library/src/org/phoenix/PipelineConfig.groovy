package org.phoenix

class PipelineConfig implements Serializable {
    String harborRegistry = 'harbor.ocp1.npd.co'
    String harborProject  = 'phoenix'
    String vaultHarborPath = 'secret/phoenix/ci/harbor'
    String vaultGitPath    = 'secret/phoenix/ci/git'
    String kanikoImage     = 'gcr.io/kaniko-project/executor:v1.23.2'

    String imageRef(String serviceName, String tag) {
        return "${harborRegistry}/${harborProject}/${serviceName}:${tag}"
    }
}
