$sharePath = "\\HSTNTDM01.Healthspring.Inside"

Write-Output "Checking access to $sharePath..."
Get-ChildItem -Path $sharePath


$sharePath = "\\HSTNTDM01.Healthspring.Inside"

Write-Output "Listing contents of $sharePath..."
[System.IO.Directory]::GetDirectories($sharePath)



$sharePath = "\\HSTNTDM01.Healthspring.Inside\TDM_SQL2TD"
Get-ChildItem -Path $sharePath
