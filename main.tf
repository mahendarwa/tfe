name: crs-api

on:
  workflow_dispatch:
    inputs:
      subenv:
        description: 'Subscription environment type'
        required: true
        type: choice
        options:
          - nonprod
          - prod
      location:
        description: 'CRS instance location'
        required: true
        type: choice
        options:
          - eastus
          - centralus

jobs:
  analyze:
    runs-on: [uhg-runner]

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set environment variables
        run: |
          echo "AZURE_SUBSCRIPTION=$(if [[ ${{ github.event.inputs.subenv }} == 'prod' ]]; then echo 'crs-azure-prod-sp'; else echo 'crs-azure-nonprod-sp'; fi)" >> $GITHUB_ENV
          echo "IMAGE_PATH=$(if [[ ${{ github.event.inputs.subenv }} == 'prod' ]]; then echo 'crsprodbootstrapreg.eastus.azurecr.io'; else echo 'crsnonprodbootstrapreg.eastus.azurecr.io'; fi)" >> $GITHUB_ENV
          echo "CONTAINER_REGISTRY=$(if [[ ${{ github.event.inputs.subenv }} == 'prod' ]]; then echo 'crs-prod-con-reg'; else echo 'crs-nonprod-con-reg'; fi)" >> $GITHUB_ENV
          echo "SUBSCRIPTION_ID=$(if [[ ${{ github.event.inputs.subenv }} == 'prod' ]]; then echo '5b02df11'; else echo 'e0e5bf14'; fi)" >> $GITHUB_ENV
          echo "RESOURCE_GROUP=crs-${{ github.event.inputs.subenv }}-shared-${{ github.event.inputs.location }}-rg" >> $GITHUB_ENV

      - name: Set up Maven and Java
        run: |
          echo "Setting up Java and Maven"
          ls -la /tools/java/
          export JAVA_HOME=/tools/java/jdk17
          export PATH=$JAVA_HOME/bin:$PATH
          mvn -v
          java -version
          env | grep -e PATH -e JAVA_HOME

      - name: Build the application
        run: |
          mvn clean package
