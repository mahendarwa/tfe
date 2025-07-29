$allResults = @()
$firstRun = $true
$sendCursor = $null
$hasNextPage = $true

Do {
    # Prepare GraphQL query without over-restrictive filters
    $query = @"
query GraphSearch(\$first: Int = 1000, \$sendCursor: String) {
  graphSearch(
    first: \$first
    after: \$sendCursor
    query: {
      type: [VIRTUAL_MACHINE, VIRTUAL_DESKTOP, VIRTUAL_WORKSTATION]
      select: true
    }
  ) {
    pageInfo {
      endCursor
      hasNextPage
    }
    nodes {
      id
      name
      nativeType
      isEphemeral
    }
  }
}
"@

    $queryBody = @{ query = $query } | ConvertTo-Json -Compress

    $response = Invoke-RestMethod 'https://api.us81.app.wiz.io/graphql' `
        -Method POST -Headers $headers -Body $queryBody

    # Extract and append nodes
    $nodes = $response.data.graphSearch.nodes
    if ($nodes) {
        $allResults += $nodes
        Write-Host "Fetched $($allResults.Count) so far..."
    }

    # Update pagination variables
    $sendCursor = $response.data.graphSearch.pageInfo.endCursor
    $hasNextPage = $response.data.graphSearch.pageInfo.hasNextPage

} while ($hasNextPage -eq $true -and $null -ne $sendCursor)

# Export only if we have results
if ($allResults.Count -gt 0) {
    $allResults | Export-Csv -Path "C:\Users\c880938\Downloads\wizcloudRes.csv" -NoTypeInformation
    Write-Host "Export complete: $($allResults.Count) records saved."
} else {
    Write-Host "No results found."
}
