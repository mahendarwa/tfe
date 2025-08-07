sudo rsync -av --delete /opt/versions/python/ /tmp/python_copy/ && \
sudo mkdir -p /pythonPROD/python && \
cd /tmp/python_copy && \
sudo find . -type d -exec mkdir -p /pythonPROD/python/{} \; && \
sudo find . -type f -exec cp {} /pythonPROD/python/{} \;
