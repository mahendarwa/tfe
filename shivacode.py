stage('Start service') {
  agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }

  steps {
    script {
      def remoteScriptContent = """
        #!/bin/bash
        nohup ~/startPATservice_${params.prod_envi}.sh > service.log 2>&1 &
      """

      // Save script to workspace
      writeFile file: 'remote_start_service.sh', text: remoteScriptContent

      // Remove previous files and copy new scripts + jar using working ssh key
      sh "ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfmgrap@${env.server}.enterprisenet.org 'rm -rf ~/caseservice-PAT.jar'"
      sh "ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfmgrap@${env.server}.enterprisenet.org 'cp /${params.prod_envi}/bin/caseservice-PAT.jar ~/'"

      sh "ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfmgrap@${env.server}.enterprisenet.org 'rm -rf ~/startPATservice_${params.prod_envi}.sh'"
      sh "ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfmgrap@${env.server}.enterprisenet.org 'cp /${params.prod_envi}/bin/startPATservice_${params.prod_envi}.sh ~/'"

      // Copy and run script remotely
      sh "scp -o StrictHostKeyChecking=no -i ~/.ssh/vscode remote_start_service.sh pfmgrap@${env.server}.enterprisenet.org:~/"
      sh "ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfmgrap@${env.server}.enterprisenet.org 'chmod +x ~/remote_start_service.sh && bash ~/remote_start_service.sh'"
    }
  }
}
