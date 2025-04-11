- name: 🔌 Test Teradata connection using BTEQ
  run: |
    echo "🔍 Checking Teradata login to ${TERADATA_HOST}..."
    bteq <<EOF
    .logon ${TERADATA_HOST}/${TERADATA_USER},${TERADATA_PASSWORD};
    SELECT CURRENT_DATE;
    .logoff;
    .quit;
EOF
