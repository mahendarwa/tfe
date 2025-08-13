- name: DEV,QA,INT,UAT Change environment env.id.upper variable in param files
  ansible.builtin.shell: |
    if [ -d "/python{{ env }}/python/paramfiles" ]; then
      find /python{{ env }}/python/paramfiles -type f -exec sed -i -e "s/\${env.id.upper}_{{ env }}/g" {} \;
    else
      echo "Directory /python{{ env }}/python/paramfiles not found; skipping."
    fi
  args:
    executable: /bin/bash
  when: env in ["DEV", "QA", "INT", "UAT"]
  retries: 3
  delay: 3
  register: result_11
  until: result_11 is succeeded
