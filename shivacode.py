name: AKS Deploy

on:
  workflow_dispatch:
    inputs:
      releasename:
        description: 'Select the Environment'
        required: true
        type: choice
        options:
          - usdev-deploy
          - usqa-deploy
          - uat-deploy
          - ushotfix-deploy
          - euperf-deploy
          - usprod-deploy
          - euprod-deploy
          - calatam-deploy
          - apac-deploy
      releaseversion:
        description: 'Chart version' 
        required: true
        type: string
      operation:
        description: 'Operation to be carried out using deployment tool'
        required: true
        type: choice
        options:
          - deploy
          - deployuninstall

jobs:
  validate-actor:
    runs-on: self-hosted
    steps:
      - name: Validate Actor
        env:
          USER1: ${{ secrets.USER1_TOKEN }}
          USER2: ${{ secrets.USER2_TOKEN }}
          USER3: ${{ secrets.USER3_TOKEN }}
          USER4: ${{ secrets.USER4_TOKEN }}
          USER5: ${{ secrets.USER5_TOKEN }}
          USER6: ${{ secrets.USER6_TOKEN }}
          USER7: ${{ secrets.USER7_TOKEN }}
          USER8: ${{ secrets.USER8_TOKEN }}
        run: |
          if [[ "${{ github.actor }}" != "$USER1" && \
                "${{ github.actor }}" != "$USER2" && \
                "${{ github.actor }}" != "$USER3" && \
                "${{ github.actor }}" != "$USER4" && \
                "${{ github.actor }}" != "$USER5" && \
                "${{ github.actor }}" != "$USER6" && \
                "${{ github.actor }}" != "$USER7" && \
                "${{ github.actor }}" != "$USER8" ]]; then
            echo "Unauthorized actor: ${{ github.actor }}"
            exit 1
          fi
          echo "Authorized actor: ${{ github.actor }}"

  usdev:
    if: ${{ inputs.releasename == 'usdev-deploy' }}
    uses: niq-actions/aks/.github/workflows/helm.yaml@main
    secrets: inherit
    with:
      cluster: SC-02-NONPROD-EASTUS2
      namespace: omni2-dev-us-eastus2
      releasename: ${{ inputs.releasename }}
      releaseversion: ${{ inputs.releaseversion }}
      tool: helm
      operation: ${{ inputs.operation }}
      serviceprincipal: OMNSHO-SP-NP

  usqa:
    if: ${{ inputs.releasename == 'usqa-deploy' }}
    uses: niq-actions/aks/.github/workflows/helm.yaml@main
    secrets: inherit
    with:
      cluster: SC-02-NONPROD-EASTUS2
      namespace: omni2-qa-us-eastus2
      releasename: ${{ inputs.releasename }}
      releaseversion: ${{ inputs.releaseversion }}
      tool: helm
      operation: ${{ inputs.operation }}
      serviceprincipal: OMNSHO-SP-NP

  usuat:
    if: ${{ always() && github.event.inputs.releasename == 'uat-deploy' }}
    needs: validate-actor
    uses: niq-actions/aks/.github/workflows/helm.yaml@main
    secrets: inherit
    with:
      cluster: SC-02-NONPROD-EASTUS2
      namespace: omni2-uat-us-eastus2
      releasename: usuat-deploy
      releaseversion: ${{ inputs.releaseversion }}
      tool: helm
      operation: ${{ inputs.operation }}
      serviceprincipal: OMNSHO-SP-NP

  euuat:
    if: ${{ always() && github.event.inputs.releasename == 'uat-deploy' }}
    needs: validate-actor
    uses: niq-actions/aks/.github/workflows/helm.yaml@main
    secrets: inherit
    with:
      cluster: SC-02-NONPROD-WESTEUROPE
      namespace: omni2-uat-eu-westeurope
      releasename: euuat-deploy
      releaseversion: ${{ inputs.releaseversion }}
      tool: helm
      operation: ${{ inputs.operation }}
      serviceprincipal: CSASECD-SP-NP

  usperf:
    if: ${{ always() && github.event.inputs.releasename == 'uat-deploy' }}
    needs: validate-actor
    uses: niq-actions/aks/.github/workflows/helm.yaml@main
    secrets: inherit
    with:
      cluster: SC-02-NONPROD-EASTUS2
      namespace: omni2-perf-us-eastus2
      releasename: usperf-deploy
      releaseversion: ${{ inputs.releaseversion }}
      tool: helm
      operation: ${{ inputs.operation }}
      serviceprincipal: OMNSHO-SP-NP

  uat-deploy:
    if: ${{ inputs.releasename == 'uat-deploy' }}
    needs: [validate-actor, usuat, euuat, usperf]
    runs-on: ubuntu-latest
    steps:
      - run: echo "✅ UAT deployment triggered for usuat, euuat, and usperf."

  ushotfix:
    if: ${{ inputs.releasename == 'ushotfix-deploy' }}
    needs: validate-actor
    uses: niq-actions/aks/.github/workflows/helm.yaml@main
    secrets: inherit
    with:
      cluster: SC-02-NONPROD-EASTUS2
      namespace: omni2-perf-us-eastus2
      releasename: ${{ inputs.releasename }}
      releaseversion: ${{ inputs.releaseversion }}
      tool: helm
      operation: ${{ inputs.operation }}
      serviceprincipal: OMNSHO-SP-NP
      overridetargetconfig: ushotfix

  euperf:
    if: ${{ inputs.releasename == 'euperf-deploy' }}
    needs: validate-actor
    uses: niq-actions/aks/.github/workflows/helm.yaml@main
    secrets: inherit
    with:
      cluster: SC-02-NONPROD-WESTEUROPE
      namespace: omni2-perf-eu-westeurope
      releasename: ${{ inputs.releasename }}
      releaseversion: ${{ inputs.releaseversion }}
      tool: helm
      operation: ${{ inputs.operation }}
      serviceprincipal: CSASECD-SP-NP

  usprod:
    if: ${{ inputs.releasename == 'usprod-deploy' }}
    needs: validate-actor
    uses: niq-actions/aks/.github/workflows/helm.yaml@main
    secrets: inherit
    with:
      cluster: SC-02-PROD-EASTUS2
      namespace: omni2-prod-us-eastus2
      releasename: ${{ inputs.releasename }}
      releaseversion: ${{ inputs.releaseversion }}
      tool: helm
      operation: ${{ inputs.operation }}
      serviceprincipal: OMNSHO-SP-PROD

  euprod:
    if: ${{ inputs.releasename == 'euprod-deploy' }}
    needs: validate-actor
    uses: niq-actions/aks/.github/workflows/helm.yaml@main
    secrets: inherit
    with:
      cluster: SC-02-PROD-WESTEUROPE
      namespace: omni2-prod-eu-westeurope
      releasename: ${{ inputs.releasename }}
      releaseversion: ${{ inputs.releaseversion }}
      tool: helm
      operation: ${{ inputs.operation }}
      serviceprincipal: CSASECD-SP-PROD

  calatamprod:
    if: ${{ inputs.releasename == 'calatam-deploy' }}
    needs: validate-actor
    uses: niq-actions/aks/.github/workflows/helm.yaml@main
    secrets: inherit
    with:
      cluster: SC-02-PROD-EASTUS2
      namespace: omni2-prod-calatam-eastus2
      releasename: ${{ inputs.releasename }}
      releaseversion: ${{ inputs.releaseversion }}
      tool: helm
      operation: ${{ inputs.operation }}
      serviceprincipal: DISHSC-SP-PROD

  apacprod:
    if: ${{ inputs.releasename == 'apac-deploy' }}
    needs: validate-actor
    uses: niq-actions/aks/.github/workflows/helm.yaml@main
    secrets: inherit
    with:
      cluster: SC-02-PROD-SOUTHEASTASIA
      namespace: omni2-prod-ap-southeastasia
      releasename: ${{ inputs.releasename }}
      releaseversion: ${{ inputs.releaseversion }}
      tool: helm
      operation: ${{ inputs.operation }}
      serviceprincipal: PODAP-SP-PROD
