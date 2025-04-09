name: Build & Deploy Teradata via Python

on:
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest

    env:
      TD_HOST: HSTNTDDEV.HealthSpring.Inside
      TD_USER: SVP_TDM_SVC_PROD_ROLE
      TD_PASSWORD: yWSvEJ72mwbgVdUL
      PACKAGE_FILE: odms-teradata-release.tgz
      BUILD_VERSION: v1.0.${{ github.run_number }}-${{ github.sha }}

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Build Teradata Package
        run: |
          chmod +x build_teradata_package.sh
          ./build_teradata_package.sh

      - name: Extract build package
        run: |
          mkdir teradata_deploy
          tar -xzf $PACKAGE_FILE -C teradata_deploy
          find teradata_deploy

      - name: Install teradatasql (Python CLI)
        run: |
          pip install teradatasql

      - name: Deploy SQL via teradatasql
        run: |
          echo "import os, glob
import teradatasql

conn = teradatasql.connect(host=os.environ['TD_HOST'],
                           user=os.environ['TD_USER'],
                           password=os.environ['TD_PASSWORD'])

cursor = conn.cursor()
sql_files = glob.glob('teradata_deploy/src/**/*.sql', recursive=True)

for sql_file in sql_files:
    print(f'▶️ Executing: {sql_file}')
    with open(sql_file, 'r') as f:
        sql = f.read()
        try:
            cursor.execute(sql)
            print(f'✅ Success: {sql_file}')
        except Exception as e:
            print(f'❌ Failed: {sql_file} — {e}')
            exit(1)

conn.close()
" > deploy.py

          python3 deploy.py

      - name: Done
        run: echo "🎉 Deployment complete"
