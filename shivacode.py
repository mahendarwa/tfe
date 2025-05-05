- name: Merge Feature to Develop Branch
  run: |
    Branch=${{ github.event.inputs.feature_branch }}

    git config --global user.email "balaji.seetharaman@cignahealthcare.com"
    git config --global user.name "C8X6K9_Zilver"

    git fetch --all
    git checkout develop
    git reset --hard origin/develop

    git merge origin/$Branch --strategy=ours --no-edit --allow-unrelated-histories || true
    git checkout origin/$Branch -- .
    git add .
    git commit -m "Merge feature branch ($Branch) into develop, preferring feature changes"
    git push https://x-access-token:${{ secrets.MY_GITHUB_TOKEN }}@github.com/zilvertonz/GBS_DAE_Python_ETL.git develop --force
