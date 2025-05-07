

./svc.sh stop || true

./config.sh remove --unattended --token <OLD_RUNNER_TOKEN>


./config.sh --unattended \
  --url https://github.com/<your_org_or_repo_path> \
  --token <NEW_RUNNER_TOKEN> \
  --name daylnxcpsq014 \
  --labels self-hosted,Linux,X64,prod14-runner

./svc.sh install
./svc.sh start
