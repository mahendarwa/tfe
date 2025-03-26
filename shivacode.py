package wiz

default result = "pass"

allowed_caps := {
  "AUDIT_WRITE",
  "CHOWN",
  "DAC_OVERRIDE",
  "FOWNER",
  "FSETID",
  "KILL",
  "MKNOD",
  "NET_BIND_SERVICE",
  "SETFCAP",
  "SETGID",
  "SETPCAP",
  "SETUID",
  "SYS_CHROOT"
}

paths := ["containers", "initContainers"]

result = "fail" {
  some i, j, k
  container := input.spec[paths[i]][j]
  caps := container.securityContext.capabilities.add
  cap := caps[k]
  not allowed_caps[cap]
}

currentConfiguration := "securityContext.capabilities.add includes values beyond the allowed values"
expectedConfiguration := "securityContext.capabilities.add should be empty (`[]`) or contain only allowed values"
