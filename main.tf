- name: Set environment variables for Azure Key Vault access
  run: |
    echo "KEYVAULT_CLIENT_ID=${{ secrets.CRS_AZURE_CLIENT_ID_NONPROD }}" >> $GITHUB_ENV
    echo "KEYVAULT_CLIENT_SECRET=${{ secrets.CRS_AZURE_CLIENT_SECRET_NONPROD }}" >> $GITHUB_ENV
    echo "KEYVAULT_TENANT_ID=${{ secrets.CRS_AZURE_TENANT_ID_NONPROD }}" >> $GITHUB_ENV
