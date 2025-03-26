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

# Fail if any added capability is not in the allowed list
result = "fail" {
  some i, j, k
  container := input.object.spec[paths[i]][j]
  caps := container.securityContext.capabilities.add
  cap := caps[k]
  not allowed_caps[cap]
}
