- name: copy python files python-etl code to /opt/pythonetl folder using rsync
  ansible.builtin.shell: "sudo rsync -av --delete /opt/versions/python/ /python{{ env }}/python/"
  become: true
  retries: 3
  delay: 3
  register: result_8
  until: result_8 is succeeded
