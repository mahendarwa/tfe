As per your recommendation, we implemented the exclusion for AWSReservedSSO and CSS accounts in our custom policy. However, the issue count dropped from 2691 to 166, which seems too high a reduction.
We validated that only about 39 accounts are actually AWSReservedSSO or CSS — so the overall count should reduce by around 39, not more.

Could you please review the logic used in the exclusion filter and confirm if it’s applied correctly?
