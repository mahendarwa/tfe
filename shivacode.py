name: Deploy SQL to Teradata

on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Deployment environment"
        required: true
        type: choice
        options:
          - DEV
          - DEV2
          - ITE
          - INT
          - QA
          - UAT
          - PRD

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set environment variables based on input
        id: setenv
        run: |
          case "${{ github.event.inputs.environment }}" in
            DEV)
              echo "TERADATA_HOST=HSTNTDUAT.HealthSpring.Inside" >> $GITHUB_ENV
              echo "TERADATA_USER=${{ secrets.DEV_USER }}" >> $GITHUB_ENV
              echo "TERADATA_PASSWORD=${{ secrets.DEV_PASSWORD }}" >> $GITHUB_ENV
              ;;
            DEV2)
              echo "TERADATA_HOST=HSTNTDDEV.HealthSpring.Inside" >> $GITHUB_ENV
              echo "TERADATA_USER=${{ secrets.DEV2_USER }}" >> $GITHUB_ENV
              echo "TERADATA_PASSWORD=${{ secrets.DEV2_PASSWORD }}" >> $GITHUB_ENV
              ;;
            ITE)
              echo "TERADATA_HOST=HSTNTDUAT.HealthSpring.Inside" >> $GITHUB_ENV
              echo "TERADATA_USER=${{ secrets.ITE_USER }}" >> $GITHUB_ENV
              echo "TERADATA_PASSWORD=${{ secrets.ITE_PASSWORD }}" >> $GITHUB_ENV
              ;;
            INT)
              echo "TERADATA_HOST=HSTNTDUAT.HealthSpring.Inside" >> $GITHUB_ENV
              echo "TERADATA_USER=${{ secrets.INT_USER }}" >> $GITHUB_ENV
              echo "TERADATA_PASSWORD=${{ secrets.INT_PASSWORD }}" >> $GITHUB_ENV
              ;;
            QA)
              echo "TERADATA_HOST=HSTNTDUAT.HealthSpring.Inside" >> $GITHUB_ENV
              echo "TERADATA_USER=${{ secrets.QA_USER }}" >> $GITHUB_ENV
              echo "TERADATA_PASSWORD=${{ secrets.QA_PASSWORD }}" >> $GITHUB_ENV
              ;;
            UAT)
              echo "TERADATA_HOST=HSTNTDUAT.HealthSpring.Inside" >> $GITHUB_ENV
              echo "TERADATA_USER=${{ secrets.UAT_USER }}" >> $GITHUB_ENV
              echo "TERADATA_PASSWORD=${{ secrets.UAT_PASSWORD }}" >> $GITHUB_ENV
              ;;
            PRD)
              echo "TERADATA_HOST=HSTNTDPROD.HealthSpring.Inside" >> $GITHUB_ENV
              echo "TERADATA_USER=AUTOCHG_USER_CHS_PRD" >> $GITHUB_ENV
              echo "TERADATA_PASSWORD=$_bdgE7r1#Tr" >> $GITHUB_ENV
              ;;
          esac

      - name: Print config for debug
        run: |
          echo "Host: $TERADATA_HOST"
          echo "User: $TERADATA_USER"
          echo "Password length: ${#TERADATA_PASSWORD}"

      - name: Install Teradata Python client
        run: |
          pip install teradatasql

      - name: Attempt connection to Teradata
        run: |
          python3 -c "
import os
import teradatasql
print('Connecting to:', os.environ['TERADATA_HOST'])
with teradatasql.connect(host=os.environ['TERADATA_HOST'], user=os.environ['TERADATA_USER'], password=os.environ['TERADATA_PASSWORD']):
    print('✅ Connected to Teradata')
"
