Thanks for your earlier response. We did some additional review and wanted to provide more context.

The AKS login events are being captured at the subscription level through Azure Activity Logs (Event Hub 1). These reflect actions such as when a user accesses the AKS cluster from the console.

Once the user connects via kubectl exec and performs in-cluster actions (e.g., file creation or deletion), those are logged separately at the cluster level (Event Hub 2). Since these logs originate from two different Event Hubs, they currently don’t get correlated under a single event chain.
