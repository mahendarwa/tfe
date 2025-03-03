Add-WindowsFeature -Name OpenSSH-Server
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic
netsh advfirewall firewall add rule name="OpenSSH" dir=in action=allow protocol=TCP localport=22
