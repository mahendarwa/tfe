- name: Merge Feature to Develop Branch
  run: |
    Branch=${{ github.event.inputs.feature_branch }}
    git config --global user.email "balaji.seetharaman@cignahealthcare.com"
    git config --global user.name "C8X6K9_Zilver"
    git fetch origin develop
    git fetch origin ${Branch}
    git checkout -b ${Branch} origin/${Branch}
    git merge origin/develop --strategy=ours --no-edit --allow-unrelated-histories
    git push https://x-access-token:${{ secrets.MY_GITHUB_TOKEN }}@github.com/zilvertonz/GBS_DAE_Python_ETL.git HEAD:develop --force
