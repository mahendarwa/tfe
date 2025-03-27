$sharePath = "\\HSTNTDM01.Healthspring.Inside"

try {
    if (Test-Path $sharePath) {
        $folders = Get-ChildItem -Path $sharePath -Directory
        Write-Output "✅ Access to $sharePath successful. Folders:"
        $folders.Name | ForEach-Object { Write-Output " - $_" }
    } else {
        Write-Output "❌ Path not accessible or does not exist: $sharePath"
    }
}
catch {
    Write-Output "❌ Error accessing $sharePath: $_"
}
