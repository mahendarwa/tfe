name: Build & Deploy Teradata via Python

on:
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest

    env:
      TERADATA_HOST: HSTNTDDEV.HealthSpring.Inside
      TERADATA_USER: SVP_TDM_SVC_PROD_ROLE
      TERADATA_PASSWORD: yWSvEJ72mwbgVdUL
      # Optional: only required if Teradata account string is used
      # TERADATA_ACCOUNT: YOUR_ACCOUNT_NAME
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
          echo "📂 Extracted content:"
          find teradata_deploy

      - name: Install teradatasql (Python client)
        run: pip install teradatasql

      - name: Run SQL files against Teradata
        run: |
          echo "🚀 Connecting to Teradata and executing .sql files..."
          python3 <<EOF
import os, glob
import teradatasql

# Diagnostic output
print("🔍 Verifying connection values...")
print(f"HOST = {os.environ['TERADATA_HOST']}")
print(f"USER = {os.environ['TERADATA_USER']}")
print(f"PASS LEN = {len(os.environ['TERADATA_PASSWORD'])} characters")

# Check if account string is needed (uncomment if your setup requires)
# user_str = f"{os.environ['TERADATA_USER']},{os.environ['TERADATA_ACCOUNT']}"
user_str = os.environ['TERADATA_USER']

try:
    conn = teradatasql.connect(
        host=os.environ['TERADATA_HOST'],
        user=user_str,
        password=os.environ['TERADATA_PASSWORD']
    )
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)

cursor = conn.cursor()
sql_files = glob.glob('teradata_deploy/src/**/*.sql', recursive=True)

if not sql_files:
    print("⚠️ No SQL files found to execute.")
    exit(1)

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
print("🎉 All SQL files executed successfully.")
EOF

      - name: Done
        run: echo "✅ Deployment workflow completed"
