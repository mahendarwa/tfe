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
  container := input.object.spec[paths[i]][j]
  container.securityContext.capabilities.add[_] == cap
  not allowed_caps[cap]
}
