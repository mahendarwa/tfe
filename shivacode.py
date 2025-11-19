90-Day to 180-Day Custom Query Update


Hi Team,

Please find the embedded spreadsheet showing the Wiz OOTB policies and the corresponding custom queries where the 90-day checks have been updated to 180 days. All custom queries have been created and assigned severity = Info.
A quick note: in the graph queries, using enable = true works for GCP service accounts, but it does not seem to work for AWS IAM users or roles. Since these policies rely on toxic-combination graph queries, we may need to validate whether this condition is supported for AWS accounts as well.
Request you to review and confirm everything looks correct.

Thanks & Regards,
Mahendar
