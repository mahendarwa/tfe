package wiz

default result := "pass"

result := "fail" {
  input.kind == "Pod"
  val := input.metadata.labels["sidecar.istio.io/inject"]
  val == "false"
}

result := "fail" {
  input.kind == "Pod"
  val := input.metadata.annotations["sidecar.istio.io/inject"]
  val == "false"
}

currentConfiguration := sprintf("sidecar.istio.io/inject: %v", [
  input.metadata.labels["sidecar.istio.io/inject"]
])

expectedConfiguration := "sidecar.istio.io/inject: true"
