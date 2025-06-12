- name: Print length of PROD credentials
  run: |
    user="${{ secrets.PROD_USER }}"
    password="${{ secrets.PROD_PASSWORD }}"
    echo "PROD_USER length: ${#user}"
    echo "PROD_PASSWORD length: ${#password}"
  shell: bash
