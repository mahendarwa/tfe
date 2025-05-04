- name: Merge Feature to Develop Branch
  run: |
    Branch=${{ github.event.inputs.feature_branch }}
    
    git config --global user.email "balaji.seetharaman@cignahealthcare.com"
    git config --global user.name "C8X6K9_Zilver"

    git clone --branch $Branch https://x-access-token:${{ secrets.MY_GITHUB_TOKEN }}@github.com/zilvertonz/GBS_DAE_Python_ETL.git
    cd GBS_DAE_Python_ETL

    git fetch origin
    git checkout develop
    git pull origin develop

    git merge origin/$Branch --strategy-option theirs --no-edit --allow-unrelated-histories

    git push https://x-access-token:${{ secrets.MY_GITHUB_TOKEN }}@github.com/zilvertonz/GBS_DAE_Python_ETL.git develop
