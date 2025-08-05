
name: Merge feature branch

on:
  workflow_dispatch:
    inputs:
      feature_branch:
        description: 'Name of the feature branch to merge into master'
        required: true

jobs:
  merge:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout GBS_DAE_OSS repository
        uses: actions/checkout@v3
        with:
          repository: 'zilvertorz/GBS_DAE_OSS'
          token: ${{ secrets.MY_GITHUB_TOKEN }}
          ref: 'master'
          path: 'GBS_DAE_OSS'
          fetch-depth: 0

      - name: Merge feature branch into master
        run: |
          cd GBS_DAE_OSS
          git config --global user.email "abc@cignahealthcare.com"
          git config --global user.name "CBZ83G_Zilver"

          echo "Switching to master branch..."
          git checkout master
          git pull origin master

          echo "Fetching feature branch: ${{ github.event.inputs.feature_branch }}"
          git fetch origin ${{ github.event.inputs.feature_branch }}

          echo "Merging feature branch into master (auto-resolve using theirs)..."
          git merge origin/${{ github.event.inputs.feature_branch }} -X theirs --no-edit

          echo "Pushing changes to master..."
          git push origin master
