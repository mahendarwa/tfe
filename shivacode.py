stage('Kill service') {
    agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }

    steps {
        script {
            def sshCommand = """
                ssh -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i ~/.ssh/vscode ${env.adminuser}@${env.server}.enterprisenet.org '
                    echo "Connected to \$(hostname) as \$(whoami)"
                    echo " Checking for PID on port ${env.server_port} for user ${env.adminuser}..."

                    pid=\$(ps -u ${env.adminuser} -o pid= | xargs -I {} sh -c "ps -o args= -p {} | grep -q \\"Dserver.port=${env.server_port}\\" && echo {}")

                    if [ -n "\$pid" ]; then
                        echo " Found PID: \$pid. Attempting to kill..."
                        kill -9 \$pid
                        kill_status=\$?
                        if [ \$kill_status -eq 0 ]; then
                            echo "Process with PID \$pid killed successfully."
                        else
                            echo " Failed to kill PID \$pid. Exit code: \$kill_status"
                            exit 1
                        fi
                    else
                        echo " No matching process found for ${env.adminuser} on port ${env.server_port}."
                    fi
                '
            """
            sh returnStatus: true, script: sshCommand
        }
    }
}
