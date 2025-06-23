package wiz

default result = "pass"

result = "fail" {
    input.spec.type == "LoadBalancer"
    not input.metadata.annotations["service.beta.kubernetes.io/azure-load-balancer-internal"] == "true"
}

currentConfiguration := sprintf("LB annotation: '%v'", [input.metadata.annotations["service.beta.kubernetes.io/azure-load-balancer-internal"]])
expectedConfiguration := "LoadBalancer must be internal (azure-load-balancer-internal: true)"


