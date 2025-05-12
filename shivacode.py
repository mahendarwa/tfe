package wiz

default result := "pass"

is_nat_gateway := input.WizMetadata.nativeType == "compute#natGateway"

result := "fail" {
  is_nat_gateway
  input.type != "PRIVATE"
}

currentConfiguration := {
  "type": input.type
}

expectedConfiguration := {
  "type": "PRIVATE"
}
