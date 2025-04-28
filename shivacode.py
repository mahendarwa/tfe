package wiz

default result = "pass"

# List of required deny destination ranges
required_deny_ranges := { "0.0.0.0/0", "/0", "::/0" }

# Only evaluate compute firewall rules
has_required_deny {
    input.kind == "compute#firewall"
    input.direction == "EGRESS"
    some i, j
    input.denied[_].IPProtocol == "all"
    input.destinationRanges[i] == required_deny_ranges[j]
}

# Rule passes if:
# - Resource is not a firewall -> SKIP (keep pass)
# - Resource is a firewall and has required deny -> PASS
# - Resource is a firewall and does NOT have required deny -> FAIL
result = "fail" {
    input.kind == "compute#firewall"
    not has_required_deny
}
