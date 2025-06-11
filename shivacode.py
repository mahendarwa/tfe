  if: ${{ github.event.inputs.environment == 'uat-deploy' }}

      environment:
        description: 'Choose the deployment environment'
        required: true
        type: choice
        options:
          - uat-deploy
          - ushotfix-deploy
