stage('Start service') {
    agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }

    steps {
        script {
            sh """
                ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode pfnzsup3@${env.server}.enterprisenet.org '
                    echo Connected to \$(hostname) as \$(whoami)
                    cd /pfnz/bin
                    chmod +x startPATservice_${params.prod_envi}.sh
                    nohup ./startPATservice_${params.prod_envi}.sh > service.log 2>&1 &
                    echo 🚀 Service start triggered
                '
            """
        }
    }
}
