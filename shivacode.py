package wiz

default result = "pass"

required_deny_ranges := { "0.0.0.0/0", "/0", "::/0" }

has_required_deny {
    input.kind == "compute#firewall"
    input.direction == "EGRESS"
    some i, j
    input.denied[_].IPProtocol == "all"
    input.destinationRanges[i] == required_deny_ranges[j]
}

result = "fail" {
    input.kind == "compute#firewall"
    not has_required_deny
}
