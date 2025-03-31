sudo yum groupinstall "Development Tools" -y
sudo yum install gcc openssl-devel bzip2-devel libffi-devel wget -y
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
sudo tar xzf Python-3.11.0.tgz
cd Python-3.11.0
sudo ./configure --enable-optimizations
sudo make altinstall
