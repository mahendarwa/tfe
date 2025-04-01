stage('Kill PAT service on port') {
  agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }

  steps {
    script {
      def sshCommand = """
        ssh -o StrictHostKeyChecking=no pfnzsup3@daylnxcpsp023.enterprisenet.org << 'ENDSSH'
        
        echo "Finding PID for port ${env.server_port}..."

        pid=\$(ps -ef | grep 'java' | grep '-Dserver.port=${env.server_port}' | grep 'caseservice-PAT.jar' | awk '{print \$2}')

        if [ -n "\$pid" ]; then
          echo "Found PID: \$pid"
          kill -9 \$pid
          kill_status=\$?
          if [ \$kill_status -eq 0 ]; then
            echo "Successfully killed PID \$pid"
          else
            echo "Failed to kill PID \$pid (exit code \$kill_status)"
            exit 1
          fi
        else
          echo "No process found running on port ${env.server_port}."
          exit 0
        fi

        ENDSSH
      """
      sh returnStatus: true, script: sshCommand
    }
  }
}
