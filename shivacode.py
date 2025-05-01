- name: Verify Git user and remote
  run: |
    git config --global user.name "GitHub Actions"
    git config --global user.email "actions@github.com"
    git remote -v
    git ls-remote origin
