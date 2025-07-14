name: Sync from Cigna GBS_DAE_OSS to Zilverton GBS_DAE_OSS (Excluding ETL_LZ)

on:
  workflow_dispatch:

permissions:
  contents: write
  actions: write

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:

      - name: Checkout Zilverton GBS_DAE_OSS Repo
        uses: actions/checkout@v2
        with:
          repository: zilvertonz/GBS_DAE_OSS
          token: ${{ secrets.zilverton_token }}
          ref: master

      - name: Backup Workflows & ETL_LZ
        run: |
          mkdir -p backup
          cp -R .github/workflows backup/ || true
          cp -R ETL_LZ backup/ETL_LZ || true

      - name: Disable SSL Verification for Git
        run: git config --global http."https://github.sys.cigna.com".sslVerify false

      - name: Add and Fetch Cigna GBS_DAE_OSS Remote
        run: |
          git remote add cigna https://${{ github.token }}@github.sys.cigna.com/cigna/GBS_DAE_OSS.git
          git fetch cigna

      - name: Replace with Cigna Master
        run: |
          git checkout master
          git reset --hard cigna/master

      - name: Restore Workflows and ETL_LZ
        run: |
          mkdir -p .github/workflows
          cp -R backup/workflows/* .github/workflows || true
          cp -R backup/ETL_LZ ./ETL_LZ || true

      - name: Set Git Identity
        run: |
          git config --global user.name "GitHub Sync Bot"
          git config --global user.email "syncbot@example.com"

      - name: Commit Restored Folders
        run: |
          git add .github/workflows ETL_LZ
          git commit -m "Restore workflows and ETL_LZ after syncing from Cigna" || echo "No changes to commit"

      - name: Push to Zilverton Repo
        run: |
          git remote remove origin || true
          git remote add origin https://${{ secrets.zilverton_token }}@github.com/zilvertonz/GBS_DAE_OSS.git
          git push origin master --force
