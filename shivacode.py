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

invalid_hosts = hosts {
  hosts := [host |
    some i
    some j
    host := input.object.spec.servers[i].hosts[j]

    not startswith(host, concat("/", [input.namespace, ""]))
    not startswith(host, "./")
  ]

  wildcards := [host |
    some i
    some j
    host := input.object.spec.servers[i].hosts[j]
    parts := split(host, "/")
    count(parts) > 1
    startswith(parts[1], "*")
  ]

  hosts := array.concat(hosts, wildcards)
}

startswith(str, prefix) = true {
  substring(str, 0, count(prefix)) == prefix
}
