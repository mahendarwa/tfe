For subscription [add subscription ID/name here], could you please configure the following:

Enable AKS Kubernetes Audit logs under Diagnostic Settings (to capture who connects to the cluster and related activities).

Route these logs via Event Hub so that Wiz can ingest them.

As confirmed by Wiz support, when AKS diagnostic logs are streamed via Event Hub, the Kubernetes Audit log category provides the required user identity and activity details. Wiz normalizes these fields to give us visibility into actions performed within the AKS environment.
