package wiz

default result = "pass"

some container_name


result = "fail" {
    input.metadata.annotations[sprintf("container.apparmor.security.beta.kubernetes.io/%s", [container_name])] != "runtime/default"
}


result = "fail" {
    some i
    input.spec.containers[i].securityContext.appArmorProfile.type != "RuntimeDefault"
}

result = "fail" {
    input.metadata.annotations[sprintf("container.apparmor.security.beta.kubernetes.io/%s", [container_name])] == "unconfined"
}

currentConfiguration := "At least one container has a non-compliant AppArmor profile."
expectedConfiguration := "All containers should use 'runtime/default' or 'RuntimeDefault' AppArmor profiles."
