scp *.rpm user@your-server:/tmp/teradata-ttu

ssh user@your-server

cd /tmp/teradata-ttu
sudo dnf install ./teradata-libs-*.rpm ./tdicu-*.rpm ./cliv2-*.rpm -y
sudo dnf install ./bteq-*.rpm -y

bteq
