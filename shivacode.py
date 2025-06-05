- name: 🧾 Replace env.id.upper with _QA and run SQL via BTEQ
  run: |

    export ENV_ID_UPPER=QA


    sed "s/\${env.id.upper}/_QA/g" Teradata/src/DDL/SDO_EDI_834_MBR_PCP_HIST_20250709.sql > final_script.sql

    bteq <<EOF
    .logon ${TERADATA_HOST}/${TERADATA_USER},${TERADATA_PASSWORD};
    .run file=final_script.sql;
    .logoff;
    .quit;
EOF
  shell: bash
