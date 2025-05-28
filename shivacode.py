currentConfiguration := sprintf(
  "natIP(s) found: %v",
  [input.networkInterfaces[_].accessConfigs[_].natIP]
)

expectedConfiguration := "VM must not have a public IP (natIP should be omitted)"
