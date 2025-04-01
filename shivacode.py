stage('Kill PAT service on port') {
  agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }

  steps {
    script {
      def sshCommand = """
        ssh pfnzsup3@daylnxcpsp023.enterprisenet.org << 'ENDSSH'

        echo "Checking for process listening on port 8152..."

        pid=\$(lsof -i :8152 -sTCP:LISTEN -t)

        if [ -n "\$pid" ]; then
          echo "Found PID: \$pid"
          kill -9 \$pid
          status=\$?
          if [ \$status -eq 0 ]; then
            echo "Killed PID \$pid successfully"
          else
            echo "Failed to kill PID \$pid (exit code \$status)"
            exit 1
          fi
        else
          echo "No process found listening on port 8152"
        fi

        pwd
        whoami
        cd /casdf/adsfs/ || echo "Directory not found"

        ENDSSH
      """
      sh returnStatus: true, script: sshCommand
    }
  }
}
