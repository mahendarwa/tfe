sudo rm -rf /usr/local/lib/python3.6/site-packages/pip*
sudo rm -rf /usr/local/bin/pip*
curl https://bootstrap.pypa.io/pip/3.6/get-pip.py -o get-pip.py
sudo /usr/local/bin/python3 get-pip.py
/usr/local/bin/pip3 --version
