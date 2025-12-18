Hi Dan / Marty,

Thanks for confirming. Revoking Azure access will not address the Wiz finding, as the issue relates to a local OS user (Btheerth) configured on the VMs, not Azure RBAC access.

The remediation requires the VM/application owner to rotate or remove the local user in line with CVS password complexity standards. Once completed, we’ll validate closure via a Wiz rescan.

Could you please help identify the appropriate owner for the VMs in AS-RTL-USE2-DBA-DB, or confirm if the local user can be removed if no longer required?
