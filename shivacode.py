package wiz

default result = "pass"

# Fail if pod-level is false and container-level is undefined
result = "fail" {
    input.spec.securityContext.runAsNonRoot == false
    not input.spec.containers[_].securityContext.runAsNonRoot
}

# Fail if pod-level is false and container-level is false
result = "fail" {
    input.spec.securityContext.runAsNonRoot == false
    input.spec.containers[_].securityContext.runAsNonRoot == false
}

# Fail if pod-level is true and container-level is false
result = "fail" {
    input.spec.securityContext.runAsNonRoot == true
    input.spec.containers[_].securityContext.runAsNonRoot == false
}

# Fail if pod-level is not defined and container-level is false
result = "fail" {
    not input.spec.securityContext.runAsNonRoot
    input.spec.containers[_].securityContext.runAsNonRoot == false
}

# Fail if pod-level is not defined and container-level is also not defined
result = "fail" {
    not input.spec.securityContext.runAsNonRoot
    not input.spec.containers[_].securityContext.runAsNonRoot
}
