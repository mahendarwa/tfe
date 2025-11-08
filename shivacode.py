^/var/log/pods(/.*)?$


detect-unauthorized-hostpath-access-except-o11y


apiVersion: v1
kind: Pod
metadata:
  name: fim-test-default
  namespace: default
spec:
  containers:
  - name: test
    image: busybox
    command: ["/bin/sh", "-c", "sleep 3600"]
    volumeMounts:
    - name: varlog
      mountPath: /var/log/pods
      readOnly: true
  volumes:
  - name: varlog
    hostPath:
      path: /var/log/pods
      type: Directory
