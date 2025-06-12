- name: Debug secret length
  run: |
    echo "User length: ${#TERADATA_USER}"
    echo "Password length: ${#TERADATA_PASSWORD}"
    echo "Raw password for validation: [$TERADATA_PASSWORD]"
  shell: bash
