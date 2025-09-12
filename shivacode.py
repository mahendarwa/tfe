package wiz

default result = "pass"

result = "fail" {
  count(invalid_hosts) > 0
}

invalid_hosts[host] {
  some i
  some j
  server := input.spec.servers[i]
  host := server.hosts[j]

  # Condition 1: Not starting with current namespace or "./"
  not startswith(host, concat("/", [input.metadata.namespace, ""]))
  not startswith(host, "./")
}

invalid_hosts[host] {
  some i
  some j
  server := input.spec.servers[i]
  host := server.hosts[j]

  # Condition 2: Host exactly equals "*"
  host == "*"
}

invalid_hosts[host] {
  some i
  some j
  server := input.spec.servers[i]
  host := server.hosts[j]

  # Condition 3: Namespace/* pattern
  parts := split(host, "/")
  count(parts) > 1
  startswith(parts[1], "*")
}

startswith(str, prefix) {
  substring(str, 0, count(prefix)) == prefix
}

currentConfiguration := sprintf("Host values: %v", [input.spec.servers[_].hosts])
expectedConfiguration := "Host values should not start with '*' or be '*' after namespace"
