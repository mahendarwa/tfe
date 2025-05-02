sudo yum install -y curl unixODBC unixODBC-devel
curl -O https://packages.microsoft.com/rhel/8/prod/msodbcsql17-17.10.6.1-1.x86_64.rpm
sudo ACCEPT_EULA=Y yum install -y msodbcsql17-17.10.6.1-1.x86_64.rpm
odbcinst -q -d | grep "ODBC Driver 17 for SQL Server"
