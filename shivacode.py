name: Restart PAT Service

on:
  workflow_dispatch:
    inputs:
      Group:
        description: 'Select the Group'
        required: true
        type: choice
        options:
          - group1
          - group2
          - group3

jobs:
  validate-actor:
    runs-on: prod14-runner
    steps:
      - name: validate Actor
        run: |
          echo "GitHub actor: '${{ github.actor }}'"
          IFS=',' read -ra USERS <<< "${{ vars.USERS }}"
          for u in "${USERS[@]}"; do
            CLEAN_USER=$(echo "$u" | xargs)
            echo "Comparing: CLEAN_USER='$CLEAN_USER' vs github.actor='${{ github.actor }}'"
            if [[ "$CLEAN_USER" == "${{ github.actor }}" ]]; then
              echo "✅ Authorized actor: $CLEAN_USER"
              exit 0
            fi
          done
          echo "❌ Unauthorized actor: ${{ github.actor }}"
          exit 1

  Patservice-restart:
    needs: validate-actor
    runs-on: prod14-runner
    steps:
      - name: Select environments for group
        id: select_group
        run: |
          if [[ "${{ github.event.inputs.Group }}" == "group1" ]]; then
            GROUP_ENVIRONMENTS=(pfnz pfid pfth pfph pfsg pfhk pfau pfbp omau)
          elif [[ "${{ github.event.inputs.Group }}" == "group2" ]]; then
            GROUP_ENVIRONMENTS=(pfgb pffi pfpt pfes pfra pffr pfde pfch pfit)
          elif [[ "${{ github.event.inputs.Group }}" == "group3" ]]; then
            GROUP_ENVIRONMENTS=(omca pfca pfco pfpr pfcl pfbr pfmx pfxu pfus)
          else
            echo "Invalid group selection"
            exit 1
          fi
          echo "GROUP_ENVIRONMENTS=${GROUP_ENVIRONMENTS[@]}" >> $GITHUB_ENV

      - name: Run Restart PAT Service for each environment
        run: |
          declare -A ADMINUSERS=(
            [pfnz]=pfnzsup3 [pfid]=pfidsup3 [pfph]=pfphsup3 [pfth]=pfthsup3 [pfsg]=pfsgsup3
            [pfhk]=pfhksup3 [pfau]=pfausup3 [pfbp]=pfbpsup3 [omau]=omausup3 [pfgb]=pfgbsup3
            [pffi]=pffisup3 [pfpt]=pfptsup3 [pfes]=pfessup3 [pfra]=pfrasup3 [pffr]=pffrsup3
            [pfde]=pfdesup3 [pfch]=pfchsup3 [pfit]=pfitsup3 [omca]=omcasup3 [pfca]=pfcasup3
            [pfco]=pfcosup3 [pfpr]=pfprsup3 [pfcl]=pfclsup3 [pfbr]=pfbrsup3 [pfmx]=pfmxsup3
            [pfxu]=pfxusup3 [pfus]=pfussup3
          )
          declare -A SERVERS=(
            [pfnz]=daylnxcpsp023 [pfid]=daylnxcpsp023 [pfph]=daylnxcpsp023 [pfth]=daylnxcpsp023
            [pfsg]=daylnxcpsp023 [pfhk]=daylnxcpsp023 [pfau]=daylnxcpsp023 [pfbp]=daylnxcpsp023
            [omau]=daylnxcpsp023 [pfgb]=daylnxcpsp022 [pffi]=daylnxcpsp022 [pfpt]=daylnxcpsp022
            [pfes]=daylnxcpsp022 [pfra]=daylnxcpsp022 [pffr]=daylnxcpsp022 [pfde]=daylnxcpsp022
            [pfch]=daylnxcpsp022 [pfit]=daylnxcpsp022 [omca]=daylnxcpsp014 [pfca]=daylnxcpsp014
            [pfco]=daylnxcpsp014 [pfpr]=daylnxcpsp014 [pfcl]=daylnxcpsp014 [pfbr]=daylnxcpsp014
            [pfmx]=daylnxcpsp014 [pfxu]=daylnxcpsp014 [pfus]=daylnxcpsp014
          )
          declare -A PORTS=(
            [pfnz]=8198 [pfid]=8196 [pfph]=8195 [pfth]=8197 [pfsg]=8199 [pfhk]=8200
            [pfau]=8201 [pfbp]=8203 [omau]=8202 [pfgb]=8186 [pffi]=8187 [pfpt]=8189
            [pfes]=8190 [pfra]=8188 [pffr]=8191 [pfde]=8192 [pfch]=8193 [pfit]=8194
            [omca]=8178 [pfca]=8177 [pfco]=8182 [pfpr]=8179 [pfcl]=8181 [pfbr]=8180
            [pfmx]=8183 [pfxu]=8185 [pfus]=8184
          )

          for ENV in ${GROUP_ENVIRONMENTS}; do
            ADMINUSER=${ADMINUSERS[$ENV]}
            SERVER=${SERVERS[$ENV]}
            PORT=${PORTS[$ENV]}

            echo "==============================="
            echo "Processing ENV: $ENV"
            echo "ADMINUSER: $ADMINUSER"
            echo "SERVER: $SERVER"
            echo "PORT: $PORT"
            echo "==============================="

            if [ -z "$PORT" ]; then
              echo "PORT is not set for $ENV. Skipping..."
              continue
            fi

            ssh -o StrictHostKeyChecking=no "$ADMINUSER@$SERVER.enterprisenet.org" bash <<EOSSH
            echo "Checking for process on port $PORT..."
            pid=\$(lsof -i :$PORT -sTCP:LISTEN -t)
            if [ -n "\$pid" ]; then
              echo "Found PID \$pid, killing..."
              kill -9 \$pid || exit 1
              echo "Killed PID \$pid successfully"
            else
              echo "No process found on port $PORT"
            fi

            cd /$ENV/bin || echo "Directory not found"
            nohup ./startPGPATservice_$ENV.sh > /dev/null 2>&1 &
            echo "Service restarted for $ENV"
            EOSSH

            echo "✅ Completed environment: $ENV"
            echo "==============================="

          done
