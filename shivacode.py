currentConfiguration := sprintf(
  "canIpForward: %v, natIP: %v",
  [input.canIpForward, input.networkInterfaces[_].accessConfigs[_].natIP]
)

expectedConfiguration := "VM must not have a public IP (natIP) and canIpForward must be false"
