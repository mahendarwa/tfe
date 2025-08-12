- name: Show src and dest paths for tarball
  debug:
    msg:
      - "SRC: /var/tmp/workspace/{{ lookup('ansible.builtin.env', 'VERSION') }}.tgz"
      - "DEST: /var/tmp/workspace/{{ lookup('ansible.builtin.env', 'VERSION') }}.tgz"
