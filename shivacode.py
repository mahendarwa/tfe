# Create a working directory
mkdir -p ~/teradata-ttu && cd ~/teradata-ttu

# Download the required RPMs
wget https://downloads.teradata.com/download/cdn/ttu/17.20/linux/teradata-client/teradata-libs-17.20.15.00-1.noarch.rpm
wget https://downloads.teradata.com/download/cdn/ttu/17.20/linux/teradata-client/tdicu-17.20.15.00-1.noarch.rpm
wget https://downloads.teradata.com/download/cdn/ttu/17.20/linux/teradata-client/cliv2-17.20.15.00-1.noarch.rpm
wget https://downloads.teradata.com/download/cdn/ttu/17.20/linux/teradata-client/bteq-17.20.15.00-1.noarch.rpm

# Verify files
ls -lh

# Install all downloaded RPMs
sudo dnf install ./*.rpm -y

# Test bteq
bteq
