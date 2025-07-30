package wiz

allowed_kinds := {
    "ReplicaSet",
    "DaemonSet",
    "CronJob",
    "StatefulSet",
    "Deployment",
    "Job"
}

default result := "pass"

# Fail if ownerReferences is missing
result := "fail" {
    not input.object.metadata.ownerReferences
}

# Fail if any ownerReference.kind is NOT in allowed list
result := "fail" {
    some i
    input.object.metadata.ownerReferences[i].kind
    not input.object.metadata.ownerReferences[i].kind in allowed_kinds
}

currentConfiguration := sprintf("%v", [input.object.metadata.ownerReferences])
expectedConfiguration := "Pods must be managed by one of: ReplicaSet, DaemonSet, CronJob, StatefulSet, Deployment, Job"
