Branch=${{ github.event.inputs.feature_branch }}

git config --global user.email "balaji.seetharaman@cignahealthcare.com"
git config --global user.name "C8X6K9_Zilver"

git remote set-url origin https://x-access-token:${{ secrets.MY_GITHUB_TOKEN }}@github.com/zilvertonz/GBS_DAE_Python_ETL.git
git fetch origin

git checkout develop || git checkout -b develop origin/develop
git pull origin develop

git fetch origin $Branch:$Branch || echo "Feature branch $Branch already exists locally"
git merge $Branch --strategy=ours --no-edit --allow-unrelated-histories || true

git push origin develop --force
