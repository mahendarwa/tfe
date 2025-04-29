package wiz

default result = "fail"

disallowed_ranges := {"/0", "0.0.0.0", "0.0.0.0/0", "::/0"}

has_disallowed_range {
    some i, j
    input.direction == "EGRESS"
    input.destinationRanges[i] == disallowed_ranges[j]
}

has_disallowed_range {
    some i, j
    input.direction == "INGRESS"
    input.sourceRanges[i] == disallowed_ranges[j]
}

is_deny_all {
    input.denied[_].IPProtocol == "all"
}

result = "pass" {
    input.kind == "compute#firewall"
    has_disallowed_range
    is_deny_all
}

result = "pass" {
    input.kind != "compute#firewall"
}

currentConfiguration := sprintf("Firewall rule '%s' missing DENY ALL on 0.0.0.0/0 for %s direction", [input.name, input.direction])
expectedConfiguration := "A DENY ALL rule to 0.0.0.0/0 should be present for at least one direction (ingress or egress)"
