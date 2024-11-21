- name: Delete Docker Image from ACR
  run: |
    echo "Deleting Docker image from ACR"
    az acr repository delete \
      --name crsnonprodbootstraprgastuse0e5bf14 \
      --image ${env.IMAGE_PATH}/crs/crs-api:api-${{ github.run_number }} \
      --yes
