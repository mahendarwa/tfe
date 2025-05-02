sudo su -c 'curl -s https://packages.microsoft.com/config/rhel/8/prod.repo > /etc/yum.repos.d/msprod.repo && ACCEPT_EULA=Y yum install -y msodbcsql17'
