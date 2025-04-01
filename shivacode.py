stage('Kill PAT Service') {
  agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }
  steps {
    script {
      def sshCommand = '''
        ssh pfnzsup3@daylnxcpsp023.enterprisenet.org << 'ENDSSH'
        echo "🔍 Searching for PID using port 8152 for user pfnzsup3"
        pid=$(ps -u pfnzsup3 -o pid= | xargs -I {} sh -c "ps -o args= -p {} | grep -q \\"Dserver.port=8152\\" && echo {}")
        
        if [ -n "$pid" ]; then
          echo "🔴 Found PID: $pid. Attempting to kill..."
          kill -9 $pid
          status=$?
          if [ $status -eq 0 ]; then
            echo "✅ Killed PID $pid successfully."
          else
            echo "❌ Failed to kill PID $pid (exit code $status)"
            exit $status
          fi
        else
          echo "⚠️  No process found for port 8152 under user pfnzsup3"
        fi
        ENDSSH
      '''
      sh returnStatus: true, script: sshCommand
    }
  }
}
