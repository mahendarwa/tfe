Get-ChildItem -Path "C:\Program Files\WindowsPowerShell\Modules" -Recurse -Filter Newtonsoft.Json.dll -ErrorAction SilentlyContinue |
Select-Object FullName, @{Name='Version';Expression={(Get-Item $_.FullName).VersionInfo.FileVersion}}


(Get-Item "C:\Program Files\WindowsPowerShell\Modules\Microsoft.Graph.Devices.CorporateManagement\1.9.3\bin\Newtonsoft.Json.dll").VersionInfo.FileVersion

Get-Module -ListAvailable Microsoft.Graph* | Select Name, Version


Update-Module Microsoft.Graph
Install-Module Microsoft.Graph -Force


Restart-Service WinRM

