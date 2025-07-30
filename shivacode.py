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
    some i
    not input.ownerReferences[i].kind in allowed_kinds
}


currentConfiguration := sprintf("%v", [input.ownerReferences])
expectedConfiguration := "Pods must be managed by one of: ReplicaSet, DaemonSet, CronJob, StatefulSet, Deployment, Job"
