package wiz

default result = "pass"

result = "skip" {
  input.request.object.kind != "Gateway"
} else = "skip" {
  not contains(input.request.object.apiVersion, "istio.io")
} else = "pass" {
  count(invalid_hosts) == 0
} else = "fail"

invalid_hosts[host] {
  some i
  host := input.request.object.spec.servers[i].hosts[_]
  not startswith(host, concat("/", [input.request.namespace, ""]))
  not startswith(host, "./")
}

invalid_hosts[host] {
  some i
  server := input.request.object.spec.servers[i]
  some j
  host := server.hosts[j]
  parts := split(host, "/")
  count(parts) > 1
  startswith(parts[1], "*")
}

startswith(str, prefix) {
  substring(str, 0, count(prefix)) == prefix
}

currentConfiguration := sprintf("Host values: %v", [input.request.object.spec.servers[_].hosts])
expectedConfiguration := "Host values should not start with '*' after 'namespace/*'"
