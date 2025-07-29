# Authentication headers
$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type"  = "application/json"
}

# Query parameters
$first = 100
$afterDate = "2024-06-02"
$orderBy = "DESC"

# Variables
$response = $null
$SendCursor = $null
$hasNextPage = $true

Do {
    # Set cursor value for GraphQL query
    if ($null -eq $SendCursor) {
        $cursorValue = "null"
    } else {
        $cursorValue = "`"$SendCursor`""
    }

    # Build GraphQL query string
    $query = @"
query {
  vulnerabilityFindings(first: $first, after: $cursorValue, orderBy: { field: "CREATED_AT", direction: $orderBy }, filter: { createdAt: { gt: "$afterDate" }}) {
    pageInfo {
      endCursor
      hasNextPage
    }
    nodes {
      id
      name
      severity
      createdAt
    }
  }
}
"@

    # Convert query to proper JSON payload
    $payload = @{ query = $query } | ConvertTo-Json -Compress

    # Call Wiz GraphQL API
    $response = Invoke-RestMethod 'https://api.us81.app.wiz.io/graphql' `
        -Method 'POST' `
        -Headers $headers `
        -Body $payload

    # Get pagination info
    $SendCursor = $response.data.vulnerabilityFindings.pageInfo.endCursor
    $hasNextPage = $response.data.vulnerabilityFindings.pageInfo.hasNextPage

    # Debug output
    Write-Host "Next Cursor: $SendCursor"
    Write-Host "Has Next Page: $hasNextPage"

} While ($hasNextPage -and $null -ne $SendCursor)
