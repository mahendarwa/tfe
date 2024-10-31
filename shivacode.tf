- name: Azure Login
  run: |
    az login --service-principal \
      --username "${{ secrets.AZURE_CLIENT_ID }}" \
      --password "${{ secrets.AZURE_CLIENT_SECRET }}" \
      --tenant "${{ secrets.AZURE_TENANT_ID }}"
