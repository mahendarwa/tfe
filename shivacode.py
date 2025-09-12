package wiz

default result = "pass"

result = "fail" {
  some i
  some j
  server := input.spec.servers[i]
  host := server.hosts[j]

  invalid_host(host)
}

invalid_host(host) {
  not startswith(host, concat("/", [input.metadata.namespace, ""]))
  not startswith(host, "./")
}

invalid_host(host) {
  host == "*"
}

invalid_host(host) {
  parts := split(host, "/")
  count(parts) > 1
  startswith(parts[1], "*")
}

startswith(str, prefix) {
  substring(str, 0, count(prefix)) == prefix
}

currentConfiguration := sprintf("Host values: %v", [input.spec.servers[_].hosts])
expectedConfiguration := "Host values should not be '*' or contain invalid namespace patterns"
