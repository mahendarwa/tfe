name: Teradata PVS Validation & Deployment

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
  validate-and-deploy:
    runs-on: ubuntu-latest
    env:
      BUILD_VERSION: v1.0.${{ github.run_number }}-${{ github.sha }}
      PACKAGE_FILE: odms-teradata-release.tgz
    steps:

      - name: Checkout code
        uses: actions/checkout@v4

      - name: Extract build package
        run: |
          mkdir teradata_deploy
          tar -xzf $PACKAGE_FILE -C teradata_deploy
          echo "📦 Extracted content:"
          find teradata_deploy

      - name: Validate PVS content from update.xml
        run: |
          echo "🔎 Validating update.xml references against pvs.sql..."
          python3 <<EOF
          import os

          update_path = "teradata_deploy/Teradata/src/update.xml"
          pvs_path = "teradata_deploy/Teradata/src/PVS/pvs.sql"

          if not os.path.exists(update_path):
              print(f"❌ update.xml not found at {update_path}")
              exit(1)

          if not os.path.exists(pvs_path):
              print(f"❌ pvs.sql not found at {pvs_path}")
              exit(1)

          with open(update_path, 'r') as f:
              update_lines = f.readlines()

          with open(pvs_path, 'r') as f:
              pvs_sql = f.read().upper()

          def extract_proc_name(line):
              try:
                  if 'PROC' not in line:
                      return None
                  parts = line.upper().strip().split("PROC/")
                  if len(parts) > 1:
                      proc_part = parts[1].split(".SQL")[0]
                      return proc_part.split("/")[-1] if "/" in proc_part else proc_part
              except:
                  return None

          missing = []
          for line in update_lines:
              proc = extract_proc_name(line)
              if proc and proc not in pvs_sql:
                  print(f"❌ PROC missing in pvs.sql: {proc}")
                  missing.append(proc)

          if missing:
              print("❌ Validation failed! Missing procedures:", missing)
              exit(1)

          print("✅ All referenced procedures found in pvs.sql")
          EOF

      - name: Done
        run: echo "✅ Validation complete. Ready for deployment."
