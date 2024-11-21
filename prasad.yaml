#!/usr/bin/env groovy
@Library("com.optum.jenkins.pipeline.library@master") _
import groovy.transform.Field

@Field
String dotnetEnvironment = ''

pipeline {
agent { label 'docker-maven-slave' }
    parameters{
      choice(
          name: 'subenv',
          choices: ['nonprod', 'prod'],
          description: 'Subscription environment type for deployment'
      )
       choice(
           name: 'location',
           choices: ['eastus', 'centralus'],
           description: 'CRS instance location'
       )
    }

      environment {
        azureSubscription="${params.subenv == 'prod' ? 'crs-azure-prod-sp' : 'crs-azure-nonprod-sp'}"
        imagePath="${params.subenv == 'prod' ? 'crsprodbootstraprgeastus5b02df11.azurecr.io' : 'crsnonprodbootstraprgeastuse0e5bf14.azurecr.io'}"
        containerRegistry="${params.subenv == 'prod' ? 'crs-prod-con-reg' : 'crs-nonprod-con-reg'}"
        subID="${params.subenv == 'prod' ? '5b02df11' : 'e0e5bf14'}"
        subscriptionID="${params.subenv == 'prod' ? '5b02df11-58c9-471f-8b89-812c1806b015' : 'e0e5bf14-0e68-4675-a9c1-84e450ab6f89'}"
        rg="crs-${params.subenv}-shared-${location}-rg"
    }

    tools {
        maven 'maven-mixin'
    }

    stages {
        stage('Build') {
            steps {
               sh '''
                      ls -la /tools/java/
                      export JAVA_HOME=/tools/java/jdk17
                      export PATH=$JAVA_HOME/bin:$PATH
                      mvn -v
                      java --version
                      env | grep -e PATH -e JAVA_HOME
                      mvn test
                      mvn clean package
                   '''
            }
        }

     /* stage('Sonar Scan') {
          steps {
              sh "mvn sonar:sonar -D\"sonar.projectKey=com.optum.ContentRulesStudio:cloud\" -D\"sonar.sources=.\" -D\"sonar.host.url=https://sonar.optum.com\" -Dsonar.login=\"121254e168892ffefc6180f27750a9d2364d5488\""
           }
         }*/

stage('Docker image to ACR') {

            steps {
             glAzureLogin('crs-azure-nonprod-sp') {
              glDockerImageBuildPush (
                                           credentialsId: "${containerRegistry}",
                                           image: "${imagePath}/crs/crs-api:api-${BUILD_NUMBER}",
                                          baseDir: "${WORKSPACE}",
                                          containerRegistry: "${imagePath}"
                                  )
                                  }
        }
        }

        stage ('Deploy to Azure NP') {
            agent {
                                    label 'azure-deploy'
                                }
            steps {
                    glAzureLogin("$azureSubscription") {
                      sh '''
                      set +x
                                          echo "testing1"
                                          echo "${WORKSPACE}"
                                          cat /etc/profile.d/jenkins.sh
                                          . /etc/profile.d/jenkins.sh
                                          cd ${WORKSPACE}

                                          az aks get-credentials --name crs-shared-aks-eastus-nonprod --resource-group crs-nonprod-shared-eastus-rg --admin --overwrite
                                          vault_enabled=$(az keyvault secret show --name keyvault-enabled --vault-name crs-api-vault --query value -o tsv)
                                          kayvault_tenantid=$(az keyvault secret show --name Kayvault-tenantid --vault-name crs-api-vault --query value -o tsv)
                                          keyvault_client_id=$(az keyvault secret show --name Keyvault-client-id --vault-name crs-api-vault --query value -o tsv)
                                          keyvault_clientkey=$(az keyvault secret show --name Keyvault-clientkey --vault-name crs-api-vault --query value -o tsv)
                                          mssql_acct_key=$(az keyvault secret show --name mssql-acct-key --vault-name crs-api-vault --query value -o tsv)
                                          sqlmi_db_password=$(az keyvault secret show --name sqlmi-db-password --vault-name crs-api-vault --query value -o tsv)
                                          oauth_secret_prd=$(az keyvault secret show --name oauth-secret-prd --vault-name crs-api-vault --query value -o tsv)
                                          splunk_token=$(az keyvault secret show --name splunk-token --vault-name crs-api-vault --query value -o tsv)
                                          oauthKey=$(az keyvault secret show --name oauth-public-key --vault-name crs-api-vault --query value -o tsv)
                                          oauthKeylink=$(az keyvault secret show --name oauth-publickey-link --vault-name crs-api-vault --query value -o tsv)
                                          oauthlbmAcc=$(az keyvault secret show --name lbm-pricer-AccountKey --vault-name crs-api-vault --query value -o tsv)
                                          echo "oauth-public-key $oauthKey"
                                          echo "oauth-public-key-link $oauthKeylink"
                                          echo "lbm-pricer-AccountKey $oauthlbmAcc"
                                          echo "splunk_token $splunk_token"
                                          echo "oauth_secret_prd $oauth_secret_prd"
                                          echo "mssql_acct_key $mssql_acct_key"
                                          echo "keyvault_clientkey $keyvault_clientkey"
                                          echo "keyvault_client_id $keyvault_client_id"
                                          echo "kayvault_tenantid $kayvault_tenantid"
                                          echo "vault_enabled $vault_enabled"
                                          cd ${WORKSPACE}/helm
                                          #helm upgrade -i  "crs-azure-crs-api" crs-api/ --values "value/nonprod/nonprod.yml" --set imageAPI="${imagePath}/crs/crs-api:api-${BUILD_NUMBER}" --set env="nonprod" --set spring.profiles.active="${AZURE_DEPLOY_ENVIRONMENT}" --set vaultEnabled="${vault_enabled}" --set lbm_pricer_AccountKey="${oauthlbmAcc}" --set oauth_link_publickey="${oauthKeylink}" --set keyvault_clientkey="${keyvault_clientkey}" --set keyvault_client_id="${keyvault_client_id}" --set oauth_secret_prd="${oauth_secret_prd}" --set splunk_token="${plunk_token}" --set keyvault_tenantid="${kayvault_tenantid}" --set oauth_publickey="${oauthKey}" --set oauth_mssqlacckey="${mssql-acct-key}" --set oauth_sqlmidbpasswd="${sqlmi_db_password}"
                                         # helm upgrade -i "crs-ingress" crs-ingress-api/ --values "value/nonprod/nonprod.yml" --set env="nonprod"

                      set -x
                                        '''
                    }


            }
        }
    }
}
