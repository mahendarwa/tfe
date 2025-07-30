package wiz

default result := "pass"

# Fail if ownerReferences is missing or empty
result := "fail" {
    not input.object.metadata.ownerReferences
}

currentConfiguration := sprintf("%v", [input.object.metadata.ownerReferences])
expectedConfiguration := "Pods must have ownerReferences"
