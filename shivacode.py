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

  PAT:
    needs: validate-actor
    runs-on: prod-runner
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

          echo "GROUP_ENVIRONMENTS=${GROUP_ENVIRONMENTS[@]}" >> $GITHUB_ENV

      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Run PAT steps for each environment
        run: |
          for ENV in ${GROUP_ENVIRONMENTS}; do
            echo "==============================="
            echo "Processing environment: $ENV"
            echo "==============================="

            # Set ADMIN_USR
            case "$ENV" in
              pfnz|pfid|pfph|pfth|pfsg|pfhk|pfau|pfbp|omau)
                ADMIN_USR=pfmgrap
                ;;
              pfca|omca|pfcl|pfco|pfpr|pfbr|pfmx|pfxu|pfus)
                ADMIN_USR=pfmgram
                ;;
              pffi|pfra|pfgb|pfpt|pfes|pffr|pfde|pfch|pfit)
                ADMIN_USR=pfmgreu
                ;;
              *)
                echo "Invalid environment: $ENV"
                exit 1
                ;;
            esac

            # Set PATH_ENV
            case "$ENV" in
              pfnz) PATH_ENV=AP_Region/NZ/ ;;
              pfid) PATH_ENV=AP_Region/ID/ ;;
              pfph) PATH_ENV=AP_Region/PH/ ;;
              pfth) PATH_ENV=AP_Region/TH/ ;;
              pfsg) PATH_ENV=AP_Region/SG/ ;;
              pfhk) PATH_ENV=AP_Region/HK/ ;;
              pfau) PATH_ENV=AP_Region/AU/ ;;
              pfbp) PATH_ENV=AP_Region/BP/ ;;
              omau) PATH_ENV=AP_Region/OMAU/ ;;
              pfca) PATH_ENV=CA_Region/CA/ ;;
              omca) PATH_ENV=CA_Region/OMCA/ ;;
              pfcl) PATH_ENV=LatAm_Region/CL/ ;;
              pfco) PATH_ENV=LatAm_Region/CO/ ;;
              pfpr) PATH_ENV=LatAm_Region/PR/ ;;
              pfbr) PATH_ENV=LatAm_Region/BR/ ;;
              pfmx) PATH_ENV=LatAm_Region/MX/ ;;
              pfxu) PATH_ENV=US_Region/USXU/ ;;
              pfus) PATH_ENV=US_Region/US/ ;;
              pffi) PATH_ENV=EURO_Region/FI/ ;;
              pfra) PATH_ENV=EURO_Region/RA/ ;;
              pfgb) PATH_ENV=EURO_Region/GB/ ;;
              pfpt) PATH_ENV=EURO_Region/PT/ ;;
              pfes) PATH_ENV=EURO_Region/ES/ ;;
              pffr) PATH_ENV=EURO_Region/FR/ ;;
              pfde) PATH_ENV=EURO_Region/DE/ ;;
              pfch) PATH_ENV=EURO_Region/CH/ ;;
              pfit) PATH_ENV=EURO_Region/IT/ ;;
              *)
                echo "Invalid environment: $ENV"
                exit 1
                ;;
            esac

            echo "Admin User: $ADMIN_USR"
            echo "PATH_ENV: $PATH_ENV"

            ORG_PATH="/home/jenscm1/actions-runner/_work/bcc-pat/bcc-pat/"
            TMP_PATH=/tmp/pat/
            chmod -R 755 $TMP_PATH

            REMOTE_PATHS=(
              /home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/dataimport_pat_pg/opt_64/dataimport_pat_pg
              /home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/plsegfix_pat_pg/opt_64/plsegfix_pat_pg
              /home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/plsegchk_pat_pg/opt_64/plsegchk_pat_pg
              /home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/plstatus_pat_pg/opt_64/plstatus_pat_pg
              /home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/validator_pat_pg/opt_64/validator_pat_pg
              /home/bambdev1/actions-runner/_work/bcc-pat/bcc-pat/unix/PFW_UNIX/lz4Compress/opt_64/lz4Compress
            )
            LOCAL_PATH=/tmp/actions/

            for REMOTE in "${REMOTE_PATHS[@]}"; do
              scp -r -o StrictHostKeyChecking=no -i ~/.ssh/vscode bambdev1@daylnxcpsd004:$REMOTE $LOCAL_PATH || echo "Skipping $REMOTE due to permission error"
            done

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

            echo "✅ Completed environment: $ENV"
            echo "==============================="

          done
