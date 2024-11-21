- name: Delete Docker Image from ACR
  run: |
    echo "Deleting Docker image from ACR"
    az acr repository delete \
      --name crsnonprodbootstraprgastuse0e5bf14 \
      --image crs-api-api:${{ github.run_number }} \
      --yes
