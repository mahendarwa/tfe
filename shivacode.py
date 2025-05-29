- name: Configure Git
  run: |
    release_branch="${{ github.event.inputs.release_branch }}"
    feature_branch="${{ github.event.inputs.feature_branch }}"

    git config --global user.email "Basireddygari.Manvitha@cignahealthcare.com"
    git config --global user.name "C8Z3Q5_Zilver"

    cd GBS_DAE_OSS
    git fetch origin

    git checkout -b "$feature_branch"

    git config pull.rebase false
    git config pull.ff false

    git pull origin "$feature_branch" --allow-unrelated-histories || {
      echo "⚠️ Merge conflict detected. Resolving by preferring incoming branch (theirs)..."
      git checkout --theirs .
      git add .
      git commit -m "🔧 Auto-resolved merge conflicts using remote branch (theirs)"
    }

    echo "feature_branch=$feature_branch" >> $GITHUB_ENV
    echo "release_branch=$release_branch" >> $GITHUB_ENV
