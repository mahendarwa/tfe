steps:
  - name: Checkout Code
    uses: actions/checkout@v3
    with:
      ref: feature/test_pipeline # Ensure the correct branch is checked out

  - name: Push to release
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    run: |
      ls
      pwd

      echo "Checking current branch..."
      git branch

      # Get the current date and construct the branch name
      DATE=$(date +%Y%m%d)
      Branch=release-${DATE}-python

      # Configure Git user
      git config --global user.email "balaji.seetharman@cignahealthcare.com"
      git config --global user.name "C8X6K9_Zilver"

      # Create and switch to a new branch if it doesn't exist
      if git rev-parse --verify $Branch >/dev/null 2>&1; then
        echo "Branch $Branch already exists. Switching to it."
        git checkout $Branch
      else
        echo "Creating and switching to branch $Branch."
        git checkout -b $Branch
      fi

      pwd
      ls

      echo "Creating a test file for demonstration..."
      touch t.text

      echo "Adding and committing changes..."
      if [ -n "$(git status --porcelain)" ]; then
        git add .
        git commit -m "new release"
        echo "Pushing changes to the remote branch $Branch."
        git push origin $Branch --force
      else
        echo "No changes to commit."
      fi
