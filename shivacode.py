stage('Kill PAT service on port') {
  agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }

  steps {
    script {
      def sshCommand = '''
        ssh pfnzsup3@daylnxcpsp023.enterprisenet.org << 'ENDSSH'
        echo "🔍 Checking for PID using port 8152 for user pfnzsup3..."
        pid_list=$(ps -u pfnzsup3 -o pid= | xargs -I {} sh -c 'ps -o args= -p {} | grep "Dserver.port=8152" >/dev/null && echo {}')
        if [ -n "$pid_list" ]; then
          echo "✅ Found PID(s): $pid_list. Attempting to kill..."
          for pid in $pid_list; do
            kill -9 "$pid"
            status=$?
            if [ $status -eq 0 ]; then
              echo "🗡️  Killed PID $pid successfully."
            else
              echo "❌ Failed to kill PID $pid (exit code $status)"
              exit 1
            fi
          done
        else
          echo "⚠️  No PID found using port 8152 under user pfnzsup3."
        fi
        ENDSSH
      '''

      sh returnStatus: true, script: sshCommand
    }
  }
}
