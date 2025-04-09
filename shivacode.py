name: Build & Deploy Teradata Package (DEV)

on:
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    env:
      TERADATA_HOST: HSTNTDDEV.HealthSpring.Inside
      TERADATA_USER: SVP_TDM_SVC_PROD_ROLE
      TERADATA_PASSWORD: yWSvEJ72mwbgVdUL
      PACKAGE_FILE: odms-teradata-release.tgz
      BUILD_VERSION: v1.0.${{ github.run_number }}-${{ github.sha }}

    steps:
      - name: Checkout source
        uses: actions/checkout@v4

      - name: Build Teradata Package
        run: |
          chmod +x build_teradata_package.sh
          ./build_teradata_package.sh

      - name: Extract build package
        run: |
          mkdir teradata_deploy
          tar -xzf $PACKAGE_FILE -C teradata_deploy
          echo "Extracted contents:"
          find teradata_deploy

      - name: Install Teradata CLI tools (bteq)
        run: |
          sudo apt-get update
          sudo apt-get install -y wget alien
          wget https://downloads.teradata.com/download/cdn/tools/TeradataToolsAndUtilitiesBase__ubuntu16__x86_64.deb
          sudo apt install ./TeradataToolsAndUtilitiesBase__ubuntu16__x86_64.deb || true
          sudo apt-get install -y bteq || true
          which bteq || echo " bteq not found — check Teradata CLI availability"

      - name: Deploy SQL files to Teradata
        run: |
          echo "🚀 Starting SQL deployment to $TERADATA_HOST ..."
          for sql in $(find teradata_deploy/src -name '*.sql'); do
            echo " Running: $sql"
            bteq <<EOF
.logon ${TERADATA_HOST}/${TERADATA_USER},${TERADATA_PASSWORD};
.run file = "$sql";
.quit;
EOF
          done

      - name: Deployment completed
        run: echo "🎉 Teradata deployment completed for version ${BUILD_VERSION}"
