stage('Start service') {
  agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }

  steps {
    script {
      def remoteScriptContent = """
        #!/bin/bash
        nohup /pfnz/home/pfnzsup3/startPATservice_${params.prod_envi}.sh > /pfnz/home/pfnzsup3/service.log 2>&1 &
      """

      writeFile file: 'remote_start_service.sh', text: remoteScriptContent

      sh "ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfmgrap@${env.server}.enterprisenet.org 'rm -f /pfnz/home/pfnzsup3/caseservice-PAT.jar'"
      sh "ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfmgrap@${env.server}.enterprisenet.org 'cp /${params.prod_envi}/bin/caseservice-PAT.jar /pfnz/home/pfnzsup3/'"

      sh "ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfmgrap@${env.server}.enterprisenet.org 'rm -f /pfnz/home/pfnzsup3/startPATservice_${params.prod_envi}.sh'"
      sh "ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfmgrap@${env.server}.enterprisenet.org 'cp /${params.prod_envi}/bin/startPATservice_${params.prod_envi}.sh /pfnz/home/pfnzsup3/'"

      sh "scp -o StrictHostKeyChecking=no -i ~/.ssh/vscode remote_start_service.sh pfmgrap@${env.server}.enterprisenet.org:/pfnz/home/pfnzsup3/"
      sh "ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfmgrap@${env.server}.enterprisenet.org 'chmod +x /pfnz/home/pfnzsup3/remote_start_service.sh'"

      sh "ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfnzsup3@${env.server}.enterprisenet.org 'bash ~/remote_start_service.sh'"
    }
  }
}
