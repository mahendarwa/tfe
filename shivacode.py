pipeline {
    agent none

    parameters {
        choice(name: 'prod_envi', choices: ['pfnz','pfid','pfph','pfsg','pfhk','pfau','pfbp','omau','pfgb','pffi','pfpt','pfes','pffr','pfde','pfch','pfit','pfra','pfca','pfco','pfpr','pfcl','pfbr','pfmx','pfxu','pfus','omca','pfth'], description: 'Select the production environment')
    }

    stages {
        stage('Map admin user') {
            steps {
                script {
                    def nameValue = params.prod_envi

                    if (nameValue == 'pfnz') {
                        env.adminuser = "pfnzsup3"
                        env.server = "daylnxcpsp023"
                        env.server_port = "8152"
                    } else if (nameValue == 'pfid') {
                        env.adminuser = "pfidsup3"
                        env.server = "daylnxcpsp023"
                        env.server_port = "8159"
                    } else if (nameValue == 'omca') {
                        env.adminuser = 'omcasup3'
                        env.server = "daylnxcpsp014"
                        env.server_port = "8151"
                    } else if (nameValue == 'pfhk') {
                        env.adminuser = 'pfhksup3'
                        env.server = "daylnxcpsp023"
                        env.server_port = "8163"
                    } else if (nameValue == 'pffi') {
                        env.adminuser = 'pffisup3'
                        env.server = "daylnxcpsp022"
                        env.server_port = "8154"
                    } else if (nameValue == 'pfco') {
                        env.adminuser = 'pfcosup3'
                        env.server = "daylnxcpsp014"
                        env.server_port = "8155"
                    } else if (nameValue == 'pfpr') {
                        env.adminuser = 'pfprsup3'
                        env.server = "daylnxcpsp014"
                        env.server_port = "8156"
                    } else if (nameValue == 'pfcl') {
                        env.adminuser = 'pfclsup3'
                        env.server = "daylnxcpsp014"
                        env.server_port = "8157"
                    } else if (nameValue == 'pfbr') {
                        env.adminuser = 'pfbrsup3'
                        env.server = "daylnxcpsp014"
                        env.server_port = "8158"
                    } else if (nameValue == 'pfca') {
                        env.adminuser = 'pfcasup3'
                        env.server = "daylnxcpsp014"
                        env.server_port = "8150"
                    } else if (nameValue == 'pfph') {
                        env.adminuser = 'pfphsup3'
                        env.server = "daylnxcpsp023"
                        env.server_port = "8160"
                    } else if (nameValue == 'pfth') {
                        env.adminuser = 'pfthsup3'
                        env.server = "daylnxcpsp023"
                        env.server_port = "8161"
                    } else if (nameValue == 'pfsg') {
                        env.adminuser = 'pfsgsup3'
                        env.server = "daylnxcpsp023"
                        env.server_port = "8162"
                    } else if (nameValue == 'pfmx') {
                        env.adminuser = 'pfmxsup3'
                        env.server = "daylnxcpsp014"
                        env.server_port = "8164"
                    } else if (nameValue == 'pfxu') {
                        env.adminuser = 'pfxusup3'
                        env.server = "daylnxcpsp014"
                        env.server_port = "8165"
                    } else if (nameValue == 'pfus') {
                        env.adminuser = 'pfussup3'
                        env.server = "daylnxcpsp014"
                        env.server_port = "8166"
                    } else if (nameValue == 'pfra') {
                        env.adminuser = 'pfrasup3'
                        env.server = "daylnxcpsp022"
                        env.server_port = "8167"
                    } else if (nameValue == 'pfgb') {
                        env.adminuser = 'pfgbsup3'
                        env.server = "daylnxcpsp022"
                        env.server_port = "8153"
                    } else if (nameValue == 'pfau') {
                        env.adminuser = 'pfausup3'
                        env.server = "daylnxcpsp023"
                        env.server_port = "8174"
                    } else if (nameValue == 'pfpt') {
                        env.adminuser = 'pfptsup3'
                        env.server = "daylnxcpsp022"
                        env.server_port = "8168"
                    } else if (nameValue == 'pfes') {
                        env.adminuser = 'pfessup3'
                        env.server = "daylnxcpsp022"
                        env.server_port = "8169"
                    } else if (nameValue == 'pffr') {
                        env.adminuser = 'pffrsup3'
                        env.server = "daylnxcpsp022"
                        env.server_port = "8170"
                    } else if (nameValue == 'pfde') {
                        env.adminuser = 'pfdesup3'
                        env.server = "daylnxcpsp022"
                        env.server_port = "8171"
                    } else if (nameValue == 'pfch') {
                        env.adminuser = 'pfchsup3'
                        env.server = "daylnxcpsp022"
                        env.server_port = "8172"
                    } else if (nameValue == 'pfit') {
                        env.adminuser = 'pfitsup3'
                        env.server = "daylnxcpsp022"
                        env.server_port = "8173"
                    } else if (nameValue == 'pfbp') {
                        env.adminuser = 'pfbpsup3'
                        env.server = "daylnxcpsp023"
                        env.server_port = "8175"
                    } else if (nameValue == 'omau') {
                        env.adminuser = 'omausup3'
                        env.server = "daylnxcpsp023"
                        env.server_port = "8176"
                    } else {
                        error("Invalid name choice: ${nameValue}")
                    }

                    env.adminuser = adminuser
                    env.server = server
                    env.server_port = server_port
                }
            }
        }

        stage('Kill PAT service on port') {
            agent { label 'consumer-panel-services-agent_prod_daylnxcpsp014' }
            steps {
                script {
                    def sshCommand = """
                        ssh ${env.adminuser}@${env.server}.enterprisenet.org << ENDSSH

                        echo "Checking for process listening on port ${env.server_port}..."

                        pid=\$(lsof -i :${env.server_port} -sTCP:LISTEN -t)

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
                          echo "No process found listening on port ${env.server_port}"
                        fi

                        pwd
                        whoami
                        cd /${params.prod_envi}/bin || echo "Directory not found"
                        nohup ./startPATservice_${params.prod_envi}.sh > /tmp/service.log 2>&1 &

                        ENDSSH
                    """
                    sh returnStatus: true, script: sshCommand
                }
            }
        }
    }
}
