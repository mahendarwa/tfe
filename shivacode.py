# Auth headers
$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type"  = "application/json"
}

$first = 100
$afterDate = "2024-06-02"
$orderBy = "DESC"

$SendCursor = $null
$hasNextPage = $true
$allResults = @()

do {
    # Format cursor
    if ($null -eq $SendCursor) {
        $cursorValue = "null"
    } else {
        $cursorValue = "`"$SendCursor`""
    }

    # GraphQL query
    $query = @"
query {
  vulnerabilityFindings(first: $first, after: $cursorValue, orderBy: { field: CREATED_AT, direction: $orderBy }, filter: { createdAt: { gt: "$afterDate" }}) {
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

    # Build JSON body
    $queryBody = @{ query = $query } | ConvertTo-Json -Compress

    # Call Wiz GraphQL API
    $response = Invoke-RestMethod 'https://api.us81.app.wiz.io/graphql' `
        -Method 'POST' `
        -Headers $headers `
        -Body $queryBody

    # Update pagination vars
    $SendCursor = $response.data.vulnerabilityFindings.pageInfo.endCursor
    $hasNextPage = $response.data.vulnerabilityFindings.pageInfo.hasNextPage

    # Store results only if present
    if ($response.data.vulnerabilityFindings.nodes) {
        $allResults += $response.data.vulnerabilityFindings.nodes
    }

    Write-Host "Fetched $($allResults.Count) so far..."

} while ($hasNextPage -and $null -ne $SendCursor)

# Export once at the end
if ($allResults.Count -gt 0) {
    $allResults | Export-Csv -Path "C:\Users\C880938\Downloads\wizcloudRes.csv" -NoTypeInformation
    Write-Host "Export complete: $($allResults.Count) records saved."
} else {
    Write-Host "No results found."
}
