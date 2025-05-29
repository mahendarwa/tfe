- name: Create teradata module
  run: |
    set -e
    set -x

    cd GBS_DAE_OSS
    git fetch origin

    if git ls-remote --exit-code --heads origin "$feature_branch"; then
      git checkout "$feature_branch"

      git config pull.rebase false
      git config pull.ff false


      git pull origin "$feature_branch" --allow-unrelated-histories || {
        echo "⚠️ Merge conflict detected. Auto-resolving using remote branch..."
        git checkout --theirs .
        git add .
        git commit -m "🔧 Auto-resolved merge conflicts using remote branch (theirs)"
      }
    else
      echo "❌ Branch $feature_branch not found in remote."
      exit 1
    fi

    ls -l
