stage('Kill service') {
    agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }

    steps {
        script {
            def sshCommand = """
                ssh -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i ~/.ssh/vscode ${env.adminuser}@${env.server}.enterprisenet.org '
                    echo "✅ Connected to \$(hostname) as \$(whoami)"
                    echo "🔍 Searching for PID with port ${env.server_port} owned by user ${env.adminuser}"

                    ps_output=\$(ps -ef | grep "[D]server.port=${env.server_port}" | grep ${env.adminuser})
                    echo "🔎 Matched ps output:"
                    echo "\$ps_output"

                    pid=\$(echo "\$ps_output" | awk "{print \\$2}")

                    if [ -n "\$pid" ]; then
                        echo "🔺 Found PID(s): \$pid"
                        echo "⚠️ Attempting to kill..."
                        kill -9 \$pid
                        kill_status=\$?
                        if [ \$kill_status -eq 0 ]; then
                            echo "✅ Process \$pid killed successfully."
                        else
                            echo "❌ Failed to kill PID \$pid. Exit code: \$kill_status"
                            exit 1
                        fi
                    else
                        echo "⚠️ No matching process found for ${env.adminuser} on port ${env.server_port}."
                    fi
                '
            """
            sh returnStatus: true, script: sshCommand
        }
    }
}
