package firewall.deny_all

default compliant = false

compliant {
    input.direction == "EGRESS"
    input.denied[_].IPProtocol == "all"
    input.destinationRanges[_] == "0.0.0.0/0"
}

compliant {
    input.direction == "INGRESS"
    input.denied[_].IPProtocol == "all"
    input.sourceRanges[_] == "0.0.0.0/0"
}
