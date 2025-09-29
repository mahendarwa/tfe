We are seeing an issue with a new CCR policy where negative test cases are not being blocked.
Working Policy: TDSTIG-GCPPLAT-CSM-02-WIZ-CCR-K8S-001
Negative test cases are blocked as expected through the admission controller policy: TD-ADMISSION-CONTROLLER-GKE-ENGLAB-BLOCK.
Issue Policy: TDSTIG-GCPPLAT-CSM-10-WIZ-CCR-K8S-001
Same Rego code and applied through the same admission controller, but negative test cases are not blocked.
Tests are run in the same GKE cluster.

Could you please help investigate why the new policy is not behaving as expected?
