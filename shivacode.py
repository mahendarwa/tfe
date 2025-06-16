package wiz

default result := "pass"

result := "fail" {
  not input.controlPlaneEndpointsConfig.ipEndpointsConfig.authorizedNetworksConfig.privateEndpointEnforcementEnabled
}

currentConfiguration := sprintf("privateEndpointEnforcementEnabled: %v", [input.controlPlaneEndpointsConfig.ipEndpointsConfig.authorizedNetworksConfig.privateEndpointEnforcementEnabled])
expectedConfiguration := "privateEndpointEnforcementEnabled: true"
