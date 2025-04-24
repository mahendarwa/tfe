package gcp.firewall

default result = "pass"

deny_reason[reason] {
  input.kind == "compute#firewall"
  input.direction == "EGRESS"
  not input.disabled
  input.destinationRanges[_] == "0.0.0.0/0"

  some i
  input.allowed[i].IPProtocol == "all"
  reason := "Firewall rule allows all protocols to 0.0.0.0/0"
}

deny_reason[reason] {
  input.kind == "compute#firewall"
  input.direction == "EGRESS"
  not input.disabled
  input.destinationRanges[_] == "0.0.0.0/0"

  some i
  input.allowed[i].ports[_] == "0-65535"
  reason := "Firewall rule allows full port range to 0.0.0.0/0"
}

result := "fail" {
  deny_reason[_]
}
