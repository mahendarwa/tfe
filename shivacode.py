$deviceCode = '<YOUR_DEVICE_CODE>'

$headers = @{
    'Content-Type' = 'application/x-www-form-urlencoded'
}

$body = "device_code=$deviceCode"

$response = Invoke-RestMethod `
  -Uri 'https://auth.app.wiz.io/api/token/device' `
  -Method POST `
  -Headers $headers `
  -Body $body `
  -UseBasicParsing

$response | ConvertTo-Json -Depth 10
