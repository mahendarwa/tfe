pipeline {
    agent any

    environment {
        WORKSPACE_BASE = "/var/lib/jenkins/workspaces"  
        MAX_WORKSPACES = 15  
    }

    stages {
        stage('Setup Workspace') {
            steps {
                script {
                    def buildNumber = currentBuild.number
                    def workspaceDir = "${WORKSPACE_BASE}/workspace_${buildNumber}"

                    echo "Creating new workspace: ${workspaceDir}"
                    sh "mkdir -p ${workspaceDir}"

                    echo "Cleaning up old workspaces..."
                    def workspaces = sh(script: "ls -td ${WORKSPACE_BASE}/workspace_* | tail -n +${MAX_WORKSPACES}", returnStdout: true).trim()
                    if (workspaces) {
                        echo "Deleting old workspaces:\n${workspaces}"
                        sh "rm -rf ${workspaces}"
                    }

                    env.WORKSPACE_DIR = workspaceDir
                }
            }
        }

        stage('Run Job') {
            steps {
                script {
                    dir(env.WORKSPACE_DIR) {
                        sh 'echo "Hello, World! This is job run #${BUILD_NUMBER}"'
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Job completed. Keeping only ${MAX_WORKSPACES} workspaces."
        }
    }
}
