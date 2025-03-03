pipeline {
    agent { label 'consumer-panel-services-agent_qa_daylnxcpsq014' }

    environment {
        WORKSPACE_BASE = "/home/bambscm1/adlm_jenkins/daylnxcpsq014/workspace/Consumer_Panel_Services_Home/Github/PAT/tes-pipeline"
        MAX_WORKSPACES = "15"
    }

    stages {
        stage('Setup Workspace') {
            steps {
                script {
                    def buildNumber = currentBuild.number
                    def workspaceDir = "${WORKSPACE_BASE}/build_${buildNumber}"

                    echo "Creating new workspace: ${workspaceDir}"
                    sh "mkdir -p '${workspaceDir}'"

                    echo "Cleaning up old workspaces..."
                    sh '''
                        WORKSPACE_BASE="/home/bambscm1/adlm_jenkins/daylnxcpsq014/workspace/Consumer_Panel_Services_Home/Github/PAT/tes-pipeline"
                        MAX_WORKSPACES=15
                        workspaces=$(ls -td ${WORKSPACE_BASE}/build_* 2>/dev/null | tail -n +$((MAX_WORKSPACES+1)))
                        if [ ! -z "$workspaces" ]; then
                            echo "Deleting old workspaces:\n$workspaces"
                            echo "$workspaces" | xargs rm -rf
                        fi
                    '''

                    env.WORKSPACE_DIR = workspaceDir
                }
            }
        }

        stage('Run Job') {
            steps {
                script {
                    dir(env.WORKSPACE_DIR) {
                        sh "echo 'Hello, World! This is job run #${BUILD_NUMBER}'"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Job completed. Keeping only ${MAX_WORKSPACES} latest builds."
        }
    }
}
