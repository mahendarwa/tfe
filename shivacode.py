- name: Set ENV_ID from input
  run: echo "ENV_ID=${{ github.event.inputs.environment }}" >> $GITHUB_ENV



executionenv = os.getenv("ENV_ID", "")
