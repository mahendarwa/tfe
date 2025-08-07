package wiz

default result = "skip"

result = "skip" {
  input.object.kind != "Gateway"
}

result = "skip" {
  not contains(input.object.apiVersion, "istio.io")
}

result = "pass" {
  count(invalid_hosts) == 0
}

result = "fail" {
  count(invalid_hosts) > 0
}

invalid_hosts := {host |
  some i
  host := input.object.spec.servers[i].hosts[_]

  # Reject if host doesn't start with expected namespace or "./"
  not startswith(host, concat("/", [input.namespace, ""]))
  not startswith(host, "./")

  # OR reject if host has wildcard "*" after namespace (e.g., "namespace/*")
} union {host |
  some i
  server := input.object.spec.servers[i]
  some j
  host := server.hosts[j]
  parts := split(host, "/")
  count(parts) > 1
  startswith(parts[1], "*")
}

startswith(str, prefix) = true {
  substring(str, 0, count(prefix)) == prefix
}

currentConfiguration := sprintf("Host values: %v", [input.object.spec.servers[_].hosts])
expectedConfiguration := "Host values should not start with '*' after 'namespace/'"
