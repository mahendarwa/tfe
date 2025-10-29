Short description:
Installation of Nginx web server on Enterprise Linux server ea4c4csap10v for Airflow reverse proxy setup.

Description:
This change is to install and configure Nginx on the target Enterprise Linux VM ea4c4csap10v using the cssacct user account. The installation will support reverse proxy configuration for Airflow (Gunicorn-based) and improve secure web access and routing.

Why this change needed / Justification:
Required to enable Airflow web UI access via Nginx reverse proxy for better scalability, SSL handling, and alignment with Airflow production recommendations.

Test plan:
Post-installation validation by accessing the Airflow web UI through Nginx on port 80 to confirm proxy functionality.

Risk and impact analysis:
Low risk. The setup is limited to one non-production VM and will not impact production workloads.

Communication plan:
Change details communicated to internal DevOps and Airflow engineering teams before implementation.

Implementation plan:
Install Nginx on server ea4c4csap10v (user: cssacct) following official Nginx RHEL installation steps documented here:
https://nginx.org/en/linux_packages.html#RHEL

Validation plan:
Confirm Nginx service startup and verify successful Airflow web UI access via reverse proxy; validation by internal team.

Backout plan:
If issues occur, stop and remove the Nginx service and revert Airflow to direct Gunicorn access on port 8080.
