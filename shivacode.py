git checkout develop
git merge ${Branch} --strategy=ours --no-edit --allow-unrelated-histories
git push https://${{ secrets.MY_GITHUB_TOKEN }}@github.com/zilvertonz/GBS_DAE_Python_ETL.git HEAD:develop --force
