package wiz

default result = "pass"

managedPodsPrefixes := {
    # EKS
    "kube-proxy-", "aws-node-", "eks-pod-identity-agent-", "coredns-",
    # AKS
    "csi-azuredisk-node-", "ama-logs-", "metrics-server-", "cloud-node-manager-",
    "konnectivity-agent-", "azure-ip-masq-agent-",
    # GKE
    "fluentbit-gke-", "pdcs-node-", "kube-dns-", "gke-metrics-agent-", "event-exporter-gke-"
}

result = "skip" {
    input.metadata.namespace == "kube-system"
    startswith(input.metadata.name, managedPodsPrefixes[_])
} else = "fail" {
    input.spec.hostNetwork == true
}

currentConfiguration := sprintf("'Pod' '%s' in '%s' namespace configured 'spec.hostNetwork': '%v'", [input.metadata.name, input.metadata.namespace, input.spec.hostNetwork])
expectedConfiguration := "Kubernetes cluster pods should only use approved host network, 'spec.hostNetwork' should be 'false'"
