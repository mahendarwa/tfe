package wiz

default result = "pass"

# Fail if any invalid host is found
result = "fail" {
  some i
  some j
  server := input.spec.servers[i]
  host := server.hosts[j]

  invalid_host(host)
}

# ---- Conditions for invalid hosts ----

# Condition 1: must not be "*" (wildcard-only host)
invalid_host(host) {
  host == "*"
}

# Condition 2: must not start with invalid namespace
invalid_host(host) {
  not startswith(host, concat("/", [input.metadata.namespace, ""]))
  not startswith(host, "./")
}

# Condition 3: namespace/* style should not allow * after "/"
invalid_host(host) {
  parts := split(host, "/")
  count(parts) > 1
  startswith(parts[1], "*")
}

# ---- Helpers ----
startswith(str, prefix) {
  substring(str, 0, count(prefix)) == prefix
}

# Debug messages (optional)
currentConfiguration := sprintf("Host values: %v", [input.spec.servers[_].hosts])
expectedConfiguration := "Host values should not contain '*' or invalid namespace patterns"
