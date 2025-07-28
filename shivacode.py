You’re setting first: 3, after: 3, but after should be set to the actual endCursor value (a string), not a number.


graphSearch(
  first: $batch,
  after: "$endCursor"
)
