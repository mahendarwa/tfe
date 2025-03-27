# Define the network share path
$sharePath = "\\HSTNTDMO1.Healthspring.Inside\TDMnonprod"

# Check if the path is accessible
if (Test-Path $sharePath) {
    Write-Host "✅ Access to the share is successful: $sharePath"
    
    # List files and folders (optional)
    Get-ChildItem $sharePath | ForEach-Object {
        Write-Host " - $_"
    }
} else {
    Write-Host "❌ Cannot access the share: $sharePath"
}
