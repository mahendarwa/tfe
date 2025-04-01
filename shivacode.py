stage('Kill PAT service') {
  agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }

  steps {
    script {
      def sshUser = env.adminuser
      def sshHost = "${env.server}.enterprisenet.org"
      def sshPort = env.server_port

      def sshCommand = """
        ssh -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i ~/.ssh/vscode ${sshUser}@${sshHost} '
          echo "🔍 Checking for PAT process on port ${sshPort} for user ${sshUser}"
          ps -ef | grep "[D]server.port=${sshPort}" | grep ${sshUser}
          pid=\$(ps -ef | grep "[D]server.port=${sshPort}" | grep ${sshUser} | awk "{print \\\$2}")
          echo "Found PID(s): \$pid"

          if [ -n "\$pid" ]; then
              echo "🔪 Killing PID \$pid..."
              kill -9 \$pid
              kill_status=\$?
              if [ \$kill_status -eq 0 ]; then
                  echo "✅ Killed PID \$pid"
              else
                  echo "❌ Failed to kill PID \$pid (code \$kill_status)"
                  exit 1
              fi
          else
              echo "⚠️ No PID found to kill for port ${sshPort} and user ${sshUser}"
          fi
        '
      """
      sh returnStatus: true, script: sshCommand
    }
  }
}
