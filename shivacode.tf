jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Git and Create Branch
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          
          DATE=$(date +%Y%m%d)
          Branch="release-${DATE}-python"
          
          git checkout -b $Branch
          git push origin $Branch
