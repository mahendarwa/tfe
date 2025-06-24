name: Prod PAT

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
    runs-on: prod-runner
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

  prepare-group:
    needs: validate-actor
    runs-on: prod-runner
    outputs:
      envs: ${{ steps.select_group.outputs.envs }}
    steps:
      - name: Select environments for group
        id: select_group
        run: |
          if [[ "${{ github.event.inputs.Group }}" == "group1" ]]; then
            GROUP_ENVIRONMENTS=(pfnz pfid pfph pfth pfsg pfhk pfau pfbp omau)
          elif [[ "${{ github.event.inputs.Group }}" == "group2" ]]; then
            GROUP_ENVIRONMENTS=(pfgb pffi pfra pfpt pfes pffr pfde pfch pfit)
          elif [[ "${{ github.event.inputs.Group }}" == "group3" ]]; then
            GROUP_ENVIRONMENTS=(omca pfca pfcl pfco pfpr pfbr pfmx pfxu pfus)
          else
            echo "Invalid group selection"
            exit 1
          fi
          echo "Selected group: ${{ github.event.inputs.Group }}"
          echo "Environments: ${GROUP_ENVIRONMENTS[@]}"
          echo "envs=$(printf '%s\n' "${GROUP_ENVIRONMENTS[@]}" | jq -R . | jq -cs .)" >> $GITHUB_OUTPUT

  PAT:
    needs: prepare-group
    runs-on: prod-runner
    strategy:
      matrix:
        environment: ${{ fromJson(needs.prepare-group.outputs.envs) }}
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set Admin User and Path
        id: set_vars
        run: |
          ENV="${{ matrix.environment }}"
          case "$ENV" in
            pfnz|pfid|pfph|pfth|pfsg|pfhk|pfau|pfbp|omau)
              echo "ADMIN_USR=pfmgrap" >> $GITHUB_ENV
              ;;
            pfca|omca|pfcl|pfco|pfpr|pfbr|pfmx|pfxu|pfus)
              echo "ADMIN_USR=pfmgram" >> $GITHUB_ENV
              ;;
            pffi|pfra|pfgb|pfpt|pfes|pffr|pfde|pfch|pfit)
              echo "ADMIN_USR=pfmgreu" >> $GITHUB_ENV
              ;;
            *)
              echo "Invalid environment: $ENV"
              exit 1
              ;;
          esac

          # Set PATH_ENV
          case "$ENV" in
            pfnz) echo "PATH_ENV=AP_Region/NZ/" >> $GITHUB_ENV ;;
            pfid) echo "PATH_ENV=AP_Region/ID/" >> $GITHUB_ENV ;;
            pfph) echo "PATH_ENV=AP_Region/PH/" >> $GITHUB_ENV ;;
            pfth) echo "PATH_ENV=AP_Region/TH/" >> $GITHUB_ENV ;;
            pfsg) echo "PATH_ENV=AP_Region/SG/" >> $GITHUB_ENV ;;
            pfhk) echo "PATH_ENV=AP_Region/HK/" >> $GITHUB_ENV ;;
            pfau) echo "PATH_ENV=AP_Region/AU/" >> $GITHUB_ENV ;;
            pfbp) echo "PATH_ENV=AP_Region/BP/" >> $GITHUB_ENV ;;
            omau) echo "PATH_ENV=AP_Region/OMAU/" >> $GITHUB_ENV ;;
            pfca) echo "PATH_ENV=CA_Region/CA/" >> $GITHUB_ENV ;;
            omca) echo "PATH_ENV=CA_Region/OMCA/" >> $GITHUB_ENV ;;
            pfcl) echo "PATH_ENV=LatAm_Region/CL/" >> $GITHUB_ENV ;;
            pfco) echo "PATH_ENV=LatAm_Region/CO/" >> $GITHUB_ENV ;;
            pfpr) echo "PATH_ENV=LatAm_Region/PR/" >> $GITHUB_ENV ;;
            pfbr) echo "PATH_ENV=LatAm_Region/BR/" >> $GITHUB_ENV ;;
            pfmx) echo "PATH_ENV=LatAm_Region/MX/" >> $GITHUB_ENV ;;
            pfxu) echo "PATH_ENV=US_Region/USXU/" >> $GITHUB_ENV ;;
            pfus) echo "PATH_ENV=US_Region/US/" >> $GITHUB_ENV ;;
            pffi) echo "PATH_ENV=EURO_Region/FI/" >> $GITHUB_ENV ;;
            pfra) echo "PATH_ENV=EURO_Region/RA/" >> $GITHUB_ENV ;;
            pfgb) echo "PATH_ENV=EURO_Region/GB/" >> $GITHUB_ENV ;;
            pfpt) echo "PATH_ENV=EURO_Region/PT/" >> $GITHUB_ENV ;;
            pfes) echo "PATH_ENV=EURO_Region/ES/" >> $GITHUB_ENV ;;
            pffr) echo "PATH_ENV=EURO_Region/FR/" >> $GITHUB_ENV ;;
            pfde) echo "PATH_ENV=EURO_Region/DE/" >> $GITHUB_ENV ;;
            pfch) echo "PATH_ENV=EURO_Region/CH/" >> $GITHUB_ENV ;;
            pfit) echo "PATH_ENV=EURO_Region/IT/" >> $GITHUB_ENV ;;
            *)
              echo "Invalid environment: $ENV"
              exit 1
              ;;
          esac

      - name: Debug Variables
        run: |
          echo "Environment: ${{ matrix.environment }}"
          echo "Admin User: ${{ env.ADMIN_USR }}"
          echo "Selected Path: $PATH_ENV"

      - name: Set Environment Variables
        run: |
          echo 'ORG_PATH="/home/jenscm1/actions-runner/_work/bcc-pat/bcc-pat/"' >> $GITHUB_ENV
          echo "TMP_PATH=/tmp/pat/" >> $GITHUB_ENV

      - name: Set Permissions for Temporary Path
        run: |
          chmod -R 755 $TMP_PATH

      - name: Set Variables
        run: |
          echo "REMOTE_PATH=/home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/dataimport_pat_pg/opt_64/dataimport_pat_pg" >> $GITHUB_ENV
          echo "REMOTE_PATH1=/home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/plsegfix_pat_pg/opt_64/plsegfix_pat_pg" >> $GITHUB_ENV
          echo "REMOTE_PATH2=/home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/plsegchk_pat_pg/opt_64/plsegchk_pat_pg" >> $GITHUB_ENV
          echo "REMOTE_PATH3=/home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/plstatus_pat_pg/opt_64/plstatus_pat_pg" >> $GITHUB_ENV
          echo "REMOTE_PATH4=/home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/validator_pat_pg/opt_64/validator_pat_pg" >> $GITHUB_ENV
          echo "REMOTE_PATH5=/home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/lz4Compress/opt_64/lz4Compress" >> $GITHUB_ENV
          echo "LOCAL_PATH=/tmp/actions/" >> $GITHUB_ENV

      - name: Copy Binary Files from Remote to Local
        run: |
          for REMOTE in $REMOTE_PATH $REMOTE_PATH1 $REMOTE_PATH2 $REMOTE_PATH3 $REMOTE_PATH4 $REMOTE_PATH5; do
            scp -r -o StrictHostKeyChecking=no -i ~/.ssh/vscode bambdev1@daylnxcpsd004:$REMOTE $LOCAL_PATH || echo "Skipping $REMOTE due to permission error"
          done

      - name: Execute SSH Commands
        env:
          ADMIN_USR: ${{ env.ADMIN_USR }}
        run: |
          ENV="${{ matrix.environment }}"
          echo "${ADMIN_USR}"
          echo "$ENV"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "chmod 750 /$ENV/bin"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "chmod -R 750 /$ENV/bin/* || true"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "cp /tmp/actions/* /$ENV/bin/"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "find ${ORG_PATH}ETL/config_pg/Production/${PATH_ENV} -type f -exec cp {} /$ENV/bin/etl/config_pg/ \;"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "cp -rf ${ORG_PATH}ETL/scripts_pg/* /$ENV/bin/etl/scripts_pg/"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "cp -rf ${ORG_PATH}ETL/sql_pg/* /$ENV/bin/etl/sql_pg/"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "cp -rf ${ORG_PATH}ETL/ref_pg/* /$ENV/bin/etl/ref_pg/"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "cp -rf ${ORG_PATH}unix/PFW_UNIX/shellscripts_pg/* /$ENV/bin/"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "chmod -R 750 /$ENV/bin/* || true"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "chmod -R 550 /$ENV/bin/* || true"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "chgrp -R $ENV /$ENV/bin/* || true"
          ssh -o StrictHostKeyChecking=no -i ~/.ssh/vscode "${ADMIN_USR}@daylnxcpsp014.enterprisenet.org" "chmod -R 550 /$ENV/bin || true"
