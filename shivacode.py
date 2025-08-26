default result := "pass"

# List of namespaces to ignore
skip_namespaces := {"kube-system", "monitoring", "logging"}

# Skip logic: if resource namespace is in skip list
result := "skip" {
    input.resource.namespace == ns
    ns := skip_namespaces[_]
}

# Fail logic
result := "fail" {
    # Add the actual failing condition here
    some condition
}
