Got it ✅ — you’ve now **moved from subscription-level to organization-level onboarding** in Wiz.
Here’s the **updated process summary** (that should replace the older document section):

---

### 🆕 Updated Wiz Account Onboarding Model

**Objective:**
To simplify onboarding and reduce manual mapping, Wiz projects now use **organization-level resource scopes** for all major clouds. Subscription-level scoping is only required for exceptions or standalone accounts.

---

### **New Model Overview**

#### **Scope 1 – Organization Level (Automatic)**

* All **GCP, Azure, and AWS** environments are now added **at the organization level**.
* Any new account under these organizations is **automatically included** in Wiz.
* Covers:

  * All-GCP (Org-based)
  * All-Azure (Org-based)
  * All-AWS (Org-based)

✅ **Purpose:** Auto-onboard all accounts under each CSP org and keep global coverage consistent.

---

#### **Scope 2 – Subscription Level (Manual, Exception Cases)**

* Used **only when**:

  * The account/project is **not part of an existing org-level integration**, or
  * It belongs to a **separate/isolated organization**.
* These are mapped manually under “Specific Subscriptions” in the **second resource scope**.

✅ **Purpose:** Handle exceptions and special cases not included in the main org mapping.

---

### **Grouping Still Required (Same 3 as Before)**

1. **Individual Line of Business (LOB)** → e.g., *Data & Analytics LOB*
2. **CSP CVS / Affiliate Grouping** → *All-GCP-CVS-Subscriptions*, *All-Azure-Affiliate*, etc.
3. **CSP Grouping by Cloud** → *All_GCP*, *All_Azure*, *All_AWS*

➡ Every account must still appear in all **three groupings**, only the **scoping method** has changed (org-level default + subscription-level fallback).

---

Would you like me to format this as a **Word/Markdown document** with your screenshots embedded and version-tagged (e.g., *“Onboarding Process v2 – Org-level Integration Model, Oct 2025”*)? That would make it ready for your internal sharepoint or Confluence upload.
