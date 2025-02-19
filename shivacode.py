/usr/local/bin/python3 --version
/usr/local/bin/python3 -m ensurepip --upgrade
curl -O https://bootstrap.pypa.io/pip/3.6/get-pip.py
/usr/local/bin/python3 get-pip.py
/usr/local/bin/python3 -m pip --version
sudo ln -s /usr/local/bin/pip3 /usr/bin/pip3
rm get-pip.py
/usr/local/bin/python3 -m pip install requests
