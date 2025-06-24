package wiz
default result = "pass"
result = "fail" {
    input.spec.type == "LoadBalancer"

    not (
        input.metadata.annotations["networking.gke.io/load-balancer-type"] == "Internal"
        or
        input.metadata.annotations["service.beta.kubernetes.io/azure-load-balancer-internal"] == "true"
    )
}
currentConfiguration := sprintf(
    "LB annotations: gke='%v', aks='%v'",
    [
        input.metadata.annotations["networking.gke.io/load-balancer-type"],
        input.metadata.annotations["service.beta.kubernetes.io/azure-load-balancer-internal"]
    ]
)
expectedConfiguration := "LoadBalancer must be internal: either GKE Internal or AKS Internal annotation"
