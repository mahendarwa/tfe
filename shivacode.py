Short description:
Delete decommissioned GCP project `prisma-13368` (ITPM ID: apm0014613)

Description:
GCP Project `prisma-13368` has been decommissioned as the associated Prisma application is no longer in use. This change removes the entire GCP project to ensure cost optimization, data hygiene, and compliance.

Justification:
Project belongs to a decommissioned Prisma application. Safe to delete as no active workloads or dependencies remain.

Test plan:
Validate project removal via:
gcloud projects list | grep prisma-13368
Ensure project no longer appears after deletion.

Risk and impact analysis:
Low risk. Project is inactive with no dependencies or integrations. No user impact expected.

Communication plan:
Stakeholders notified — Satish.Chandramohan@CVSHealth.com

Implementation plan:
1. Confirm ownership and IAM permissions for project `prisma-13368`.
2. Verify no active resources (VMs, buckets, service accounts, etc.) remain.
3. Run deletion command:
   gcloud projects delete prisma-13368
4. Validate using:
   gcloud projects list | grep prisma-13368
5. Update change ticket with confirmation.
Duration: ~45 minutes
