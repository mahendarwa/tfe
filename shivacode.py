package wiz

default result = "pass"

result = "fail" {
    count(invalid_hosts) > 0
}

invalid_hosts[host] {
    some i
    host = input.spec.servers[i].hosts[_]
    not startswith(host, concat("/", [input.metadata.namespace, ""]))
    not startswith(host, "./")
}

invalid_hosts[host] {
    some i
    server = input.spec.servers[i]
    some j
    host = server.hosts[j]
    parts := split(host, "/")
    count(parts) > 1
    startswith(parts[1], "*")
}

startswith(str, prefix) {
    substring(str, 0, count(prefix)) == prefix
}

currentConfiguration := sprintf("Host values: %v", [input.spec.servers[_].hosts])
expectedConfiguration := "Host values should not start with '*' after 'namespace/*'"
