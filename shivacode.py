Please use the below configuration for the Internal Azure Load Balancer requested for VM EAC2WIZADW10V in EastUS2.

Health Probe Details

Protocol: TCP
Port: 5432
Interval: 5 seconds
Unhealthy threshold: 2

Load Balancing Rule Details

Type: Internal Load Balancer
IP Version: IPv4
Frontend IP: Configured private frontend IP
Protocol: TCP
Frontend Port: 5432
Backend Port: 5432
Backend Pool: VM EAC2WIZADW10V
Health Probe: TCP 5432
Session Persistence: None
Idle Timeout: Default
TCP Reset: Disabled

Additional Request

Please ensure the required NSG rules are configured to allow traffic on TCP 5432 from the relevant private connectivity path/subnet.
This ILB is required in front of the VM to support the ADF/SHIR private connectivity path for PostgreSQL access.
