package aks_kspm_8

default result = "pass"

result = "fail" {
    some container
    input.metadata.annotations[sprintf("container.apparmor.security.beta.kubernetes.io/%s", [container])] != "runtime/default"
}


currentConfiguration := sprintf("At least one container has AppArmor profile set to '%s'", [input.metadata.annotations[sprintf("container.apparmor.security.beta.kubernetes.io/%s", [container])]])


expectedConfiguration := "All containers should have AppArmor profile set to 'runtime/default'"
