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


result := "fail" {
    not input.spec.ownerReferences
} else := "fail" {
    some i
    not input.spec.ownerReferences[i].kind in allowed_kinds
}

currentConfiguration := sprintf("%v", [input.spec.ownerReferences])
expectedConfiguration := "Pods must be managed by one of: ReplicaSet, DaemonSet, CronJob, StatefulSet, Deployment, Job"
