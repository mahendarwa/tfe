git fetch origin
git merge origin/develop --strategy=ours --no-edit --allow-unrelated-histories
git push https://x-access-token:${{ secrets.MY_GITHUB_TOKEN }}@github.com/zilvertonz/GBS_DAE_Python_ETL.git HEAD:${Branch} --force
