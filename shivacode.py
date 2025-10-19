Here’s the **final version** of your updated *Onboarding Cloud Accounts into Wiz Projects* document — rewritten exactly as you described (simple text, one example, org-level automation, and subscription-level exceptions):

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

**Onboarding Steps**

When onboarding new accounts (Azure subscriptions, GCP projects, AWS accounts, or OCI compartments) into Wiz, each account must be added into three Wiz projects:

1. Line of Business (LOB) Grouping
2. CSP CVS & Affiliate Grouping
3. CSP Grouping by Cloud

Since we have configured organization-level onboarding, any newly onboarded account will automatically be added to all three groups — LOB, CVS/Affiliate, and cloud-level groupings (for example, All-GCP, All-Azure, All-AWS).

Example:
edp-prod-restrict-demmdi (CVS-owned GCP project) → Data & Analytics LOB → All-GCP-CVS-Subscriptions → All_GCP

---

**Scoping Model**

Scope 1 – Organization Level (Automatic)
All GCP, Azure, and AWS organizations are added at the org level. Any account coming under these organizations will be automatically onboarded into Wiz and mapped across all three groups.

Scope 2 – Subscription Level (Manual, Exceptions Only)
Subscription-level scoping is only required for standalone or individual projects that are not part of the organization-level integration. These are manually added using the subscription scope option under Resource Scopes in Wiz.

---

Would you like me to create this as a **.docx file** with your existing screenshots (org-level and subscription-level scope views) and a clean heading layout for sharing internally?
