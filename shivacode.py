package wiz

default result := "pass"

result := "fail" {
  input["kind"] == "compute#natGateway"
  input["type"] != "PRIVATE"
}

currentConfiguration := sprintf("kind: %v, type: %v", [input.kind, input.type])
expectedConfiguration := "kind: compute#natGateway, type: PRIVATE"
