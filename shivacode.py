$accessToken = "YOUR_ACCESS_TOKEN"

$headers = @{
    "Authorization" = "bearer $accessToken"
    "Content-Type"  = "application/json"
}

$firstRun = $true
$endCursor = $null
$hasNextPage = $true
$sendCursorVal = 0

do {
    # Format the GraphQL query properly
    if ($null -eq $endCursor) {
        $cursorValue = "null"
    } else {
        $cursorValue = "`"$endCursor`""
    }

    $query = @"
query {
  vulnerabilityFindings(first: 5, after: $cursorValue) {
    pageInfo {
      endCursor
      hasNextPage
    }
    nodes {
      id
      severity
      resource {
        name
      }
    }
  }
}
"@

    # Convert to JSON format for GraphQL
    $queryBody = @{ query = $query } | ConvertTo-Json -Compress

    # Call API
    $response = Invoke-RestMethod 'https://api.us81.app.wiz.io/graphql' `
        -Method POST -Headers $headers -Body $queryBody

    $endCursor = $response.data.vulnerabilityFindings.pageInfo.endCursor
    $hasNextPage = $response.data.vulnerabilityFindings.pageInfo.hasNextPage

    $results = $response.data.vulnerabilityFindings.nodes

    # Append to CSV
    $results | Export-Csv -Path "E:\ETL\Wiz\Findings\WizCloudRes.csv" -NoTypeInformation -Append

} while ($hasNextPage -eq $true)
