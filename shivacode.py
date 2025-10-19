Here’s your updated and simplified **final version** of the *Onboarding Cloud Accounts into Wiz Projects* document — reflecting the new **organization-level model** and current **LOBs**:

---

**Onboarding Cloud Accounts into Wiz Projects**

The current LOBs in scope are:

* Data & Analytics
* Corp. Functions (Enterprise Delivery)
* HCD – Health Care Delivery
* ISTS – Information Security & Technology Solutions
* PCW – Pharmacy and Consumer Wellness
* HCB – Health Care Business
* PSS-IT (PBM) – Pharmacy Services
* PCI – PCI Applications

---

**Steps**

When onboarding new accounts (Azure subscriptions, GCP projects, AWS accounts, or OCI compartments) into Wiz, each account must be added into three Wiz projects.

Step 1 – Add to Individual Line of Business (LOB) Grouping
Place the account into the appropriate LOB folder.
Example:
edp-prod-restrict-demmdi (GCP project) → Data & Analytics LOB

Step 2 – Add to CSP CVS & Affiliate Grouping
Place the same account into the CSP CVS or Affiliate grouping based on ownership.
CVS goes into the CVS-specific grouping for that cloud.
Affiliate goes into the Affiliate grouping for that cloud.
Example:
edp-prod-restrict-demmdi (CVS-owned GCP project) → All-GCP-CVS-Subscriptions

Step 3 – Add to CSP Grouping by Cloud
Place the account into the cloud provider grouping respectively (All_AWS, All_Azure, All_GCP, All_OCI).
Example:
edp-prod-restrict-demmdi (GCP project) → All_GCP

Every new account (Azure subscriptions, GCP projects, AWS accounts, or OCI compartments) must be added in all three steps above.

---

**Updated Scoping Model**

Scope 1 – Organization Level (Automatic)
All GCP, Azure, and AWS environments are now added at the organization level. Any new account under these organizations will automatically be onboarded into Wiz.
Covers:

* All-GCP (Org-based)
* All-Azure (Org-based)
* All-AWS (Org-based)

Purpose: To automate onboarding and ensure full coverage across all accounts in the organization.

Scope 2 – Subscription Level (Manual, Exceptions Only)
Used only when the account or project is not part of the organization-level integration or belongs to a separate or isolated organization. These accounts are manually mapped under “Specific Subscriptions” in the second resource scope.

Purpose: To handle exceptions or independently managed subscriptions not linked to the primary organization-level scope.

Note: Any new account coming under an existing org-level scope is automatically added to Wiz. Only accounts that are outside org-level coverage require manual addition through subscription scope.

---

Would you like me to format this as a downloadable Word (.docx) or PDF version for upload to your SharePoint/Confluence page?
