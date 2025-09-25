# 🔹 Cluster info & config
kubectl config view
kubectl config current-context
kubectl cluster-info

# 🔹 Check if you can create pods
kubectl auth can-i create pods -n <namespace>

# 🔹 Describe resources
kubectl describe pod <pod-name> -n <namespace>
kubectl describe node <node-name>
kubectl describe deployment <deploy-name> -n <namespace>

# 🔹 Logs from a pod
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous      # previous container
kubectl logs -f <pod-name> -n <namespace>              # stream
kubectl logs <pod-name> -c <container-name> -n <namespace>

# 🔹 Exec into pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# 🔹 Test pod creation (dry-run)
kubectl run test-pod --image=nginx --dry-run=client -o yaml > test-pod.yaml
kubectl apply -f test-pod.yaml --dry-run=server
