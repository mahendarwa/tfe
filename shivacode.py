stage('Kill PAT service on port') {
  agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }
  steps {
    script {
      def sshCommand = """
        ssh \${env.adminuser}@\${env.server}.enterprisenet.org << 'ENDSSH'

        echo "Checking for process listening on port \${env.server_port}..."

        pid=\$(lsof -i :\${env.server_port} -sTCP:LISTEN -t)

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
          echo "No process found listening on port \${env.server_port}"
        fi

        pwd
        whoami
        cd /pfnz/bin || echo "Directory not found"
        nohup ./startPATservice_pfnz.sh > /tmp/service.log 2>&1 &

        ENDSSH
      """
      sh returnStatus: true, script: sshCommand
    }
  }
}
