package wiz

default result := "pass"

result := "fail" {
    some i
    input.ownerReferences[i].kind == "Pod"
}

currentConfiguration := sprintf("%v", [input.ownerReferences])
expectedConfiguration := "No Pod as ownerReference"
