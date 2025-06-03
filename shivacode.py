- name: Execute SQLs from update.xml
  run: python3 execute.py
  shell: bash
  env:
    ENV_ID: "hs"
