jobs:
  deploy:
    runs-on: zilverton-private-x64-ubuntu
    permissions:
      id-token: write
      contents: read
      packages: write
    environment: ${{ github.event.inputs.ENVIRONMENT_TYPE }}
    steps:
      - name: Checkout Code
        uses: actions/checkout@v1
        with:
          token: ${{ secrets.MY_GITHUB_TOKEN }}

      - name: Push to release
        env:
          GITHUB_TOKEN: ${{ secrets.MY_GITHUB_TOKEN }}
        run: |
          git branch
          DATE=$(date +%Y%m%d)
          Branch="release-${DATE}-python"

          git config --global user.email "balaji.seetharman@cignahealthcare.com"
          git config --global user.name "C8X6K9_Zilver"

          # Create or switch to the branch
          if git rev-parse --verify $Branch >/dev/null 2>&1; then
            git checkout $Branch
          else
            git checkout -b $Branch
          fi

          # Add and commit changes if there are any
          if [ -n "$(git status --porcelain)" ]; then
            git add .
            git commit -m "new release"
            git push origin $Branch --force
          else
            echo "No changes to commit."
          fi
