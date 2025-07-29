
 
# The GraphQL query that defines which data you wish to fetch
$query = '
query UserDocsToken {
    viewerTokens {
        docs
    }
}'

function getwizauth($client_id, $client_secret) {
    $authuri = 'https://auth.app.wiz.io/oauth/token'
    $header = @{
        Headers = @{ 'content-type' = "application/x-www-form-urlencoded" }
    }

    $tokenPayload = $access_token.Split(".")[1].Replace('-', '+').Replace('_', '/')
    while ($tokenPayload.Length % 4) { $tokenPayload += "=" }
    $tokenByteArray = [System.Convert]::FromBase64String($tokenPayload)
    $tokenArray = [System.Text.Encoding]::ASCII.GetString($tokenByteArray)
    $tokobj = $tokenArray | ConvertFrom-Json
    $dc = $tokobj.dc

    return $access_token, $dc
}

function Test-WizConnection($token, $dc) {
    $headers = @{
        "content-type" = "application/json"
        "Authorization" = "bearer " + $token
    }

    $testQuery = 'query { systemHealthIssues { totalCount } }'

    try {
        $result = Invoke-GraphQLQuery -Query $testQuery -Uri https://api.$dc.app.wiz.io/graphql -Headers $headers -ErrorAction Stop
        if ($null -ne $result.data) {
            Write-Host "✅ Successfully connected to Wiz API." -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ Connected to Wiz API but no data returned." -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host "❌ Failed to connect to Wiz API: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function query_wiz_api($token, $query, $variables, $dc) {
    $headers = @{
        "content-type" = "application/json"
        "Authorization" = "bearer " + $token
    }

    try {
        $result = Invoke-GraphQLQuery -Query $query -Variables $variables -Uri https://api.$dc.app.wiz.io/graphql -Headers $headers -ErrorAction Stop
        return $result
    }
    catch {
        Write-Host "❌ API query failed: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# --- Main Execution ---
Write-Host "Getting token..."
$token, $dc = getwizauth $client_id $client_secret

if (-not (Test-WizConnection $token $dc)) {
    Write-Host "Exiting script due to connection failure." -ForegroundColor Red
    exit
}

Write-Host "Getting data..."
$result = query_wiz_api $token $query $variables $dc

if ($null -ne $result) {
    Write-Host $result.data.systemHealthIssues.nodes
}
