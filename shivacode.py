cd /tmp/teradata-ttu

# List available RPMs to confirm what can be installed
ls -lh *.rpm

# Install all RPMs found in the current directory
sudo dnf install ./*.rpm -y
sudo dnf install ./teradata-libs-17.20.00.00-1.noarch.rpm \
                 ./tdicu-17.20.00.00-1.noarch.rpm \
                 ./cliv2-17.20.00.00-1.noarch.rpm \
                 ./bteq-17.20.00.00-1.noarch.rpm -y
