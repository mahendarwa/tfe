package wiz

default result = "pass"

# Fail if any container does not set runAsNonRoot and pod-level is also not true
result = "fail" {
    count(input.spec.containers) > 0
    some i
    container := input.spec.containers[i]
    not container.securityContext.runAsNonRoot
    not input.spec.securityContext.runAsNonRoot
}

# Fail if any container explicitly sets runAsNonRoot to false
result = "fail" {
    count(input.spec.containers) > 0
    some i
    container := input.spec.containers[i]
    container.securityContext.runAsNonRoot == false
}
