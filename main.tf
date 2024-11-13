- name: Set up environment variables
  run: |
    echo "KEYVAULT_CLIENT_ID=${{ secrets.KEYVAULT_CLIENT_ID }}" >> $GITHUB_ENV
    echo "KEYVAULT_CLIENT_KEY=${{ secrets.KEYVAULT_CLIENT_KEY }}" >> $GITHUB_ENV
    echo "KEYVAULT_TENANT_ID=${{ secrets.KEYVAULT_TENANT_ID }}" >> $GITHUB_ENV
azure.keyvault.client-id=${KEYVAULT_CLIENT_ID}
azure.keyvault.client-key=${KEYVAULT_CLIENT_KEY}
azure.keyvault.tenant-id=${KEYVAULT_TENANT_ID}
