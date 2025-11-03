We validated the recent finding reported under the path:

C:\Program Files\SplunkUniversalForwarder


After detailed verification on the VM, we confirm that Splunk Forwarder is not installed or running:

Get-Service *splunk* → No matching services found

No Splunk-related folders exist under C:\Program Files or C:\Program Files (x86)

No Splunk processes are running on the system

The directory mentioned in the finding does not exist on the host, and there are no registry or program traces of Splunk installation.
This appears to be a false positive, possibly triggered by a residual or template reference from the base image.
