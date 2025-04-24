package gcp.firewall

default result = "pass"

deny[reason] {
  input.kind == "compute#firewall"
  input.direction == "EGRESS"
  not input.disabled
  input.destinationRanges[_] == "0.0.0.0/0"
  some i
  input.allowed[i].IPProtocol == "all"  # Completely unrestricted
  reason := "Firewall rule allows all protocols to 0.0.0.0/0"
}

deny[reason] {
  input.kind == "compute#firewall"
  input.direction == "EGRESS"
  not input.disabled
  input.destinationRanges[_] == "0.0.0.0/0"
  some i
  input.allowed[i].ports[_] == "0-65535"  # Fully open port range
  reason := "Firewall rule allows full port range to 0.0.0.0/0"
}

result := "fail" {
  deny[_]
}
