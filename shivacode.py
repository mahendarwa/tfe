# Provide simple output messages
currentConfiguration := sprintf("Firewall rule '%s' is missing a DENY ALL egress rule to 0.0.0.0/0.", [input.name])
expectedConfiguration := "A DENY ALL egress rule to 0.0.0.0/0 must be present in the firewall."
