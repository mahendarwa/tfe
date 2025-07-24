name: Merge Feature Branch into Master

on:
  workflow_dispatch:
    inputs:
      feature_branch:
        description: 'Name of the feature branch to merge into master'
        required: true

jobs:
  merge:
    runs-on: zilverton-private-x64-ubuntu

    steps:
      - name: Checkout GBS_DAE_OSS repository
        uses: actions/checkout@v2
        with:
          repository: 'zilvertonz/GBS_DAE_OSS'
          token: ${{ secrets.MY_GITHUB_TOKEN }}
          ref: 'master'
          path: 'GBS_DAE_OSS'
          fetch-depth: 0

      - name: Merge feature branch into master
        run: |
          cd GBS_DAE_OSS
          git config --global user.email "a@cignahealthcare.com"
          git config --global user.name "C8230G_Zilver"
          git checkout master
          git pull origin master
          git fetch origin ${{ github.event.inputs.feature_branch }}
          git merge origin/${{ github.event.inputs.feature_branch }} --no-ff -m "Merge feature branch ${{ github.event.inputs.feature_branch }} into master"
          git push origin master
