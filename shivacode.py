package wiz

default result = "pass"

result = "fail" {
    input.spec.type == "LoadBalancer"
    not input.metadata.annotations["service.beta.kubernetes.io/azure-load-balancer-internal"] == "true"
}

currentConfiguration := sprintf("LB annotation: '%v'", [input.metadata.annotations["service.beta.kubernetes.io/azure-load-balancer-internal"]])
expectedConfiguration := "LoadBalancer must be internal (azure-load-balancer-internal: true)"

========


package wiz

default result = "pass"


result = "fail" {
    input.spec.type == "LoadBalancer"
    not input.metadata.annotations["networking.gke.io/load-balancer-type"] == "Internal"
}

currentConfiguration := sprintf(
    "LoadBalancer annotation: '%v'", 
    [input.metadata.annotations["networking.gke.io/load-balancer-type"]]
)

expectedConfiguration := "Service of type LoadBalancer must have annotation networking.gke.io/load-balancer-type: 'Internal'"

