Got it 👍 — I’ll place the **example inside each step** instead of keeping it separate at the end. That way, it’s clear exactly where the account goes in each step.

---

# 📘 Runbook: Onboarding Cloud Accounts into Wiz Project

---

## 🔹 LOBs These Are

When onboarding **new Azure subscriptions, GCP projects, AWS accounts, or OCI compartments** into Wiz, they must be mapped into the correct **LOB**.

The **LOBs** in scope are:

* **Data & Analytics**
* **Corp. Functions (Enterprise Delivery)**
* **HCD – Health Care Delivery**
* **ISTS – Information Security & Technology Solutions**
* **PCW – Pharmacy and Consumer Wellness**
* **HCB – Health Care Business**
* **PSS-IT (PBM) – Pharmacy Services**
* **PCI – PCI Applications**

---

## 🔹 Steps

Each newly onboarded account (subscription / project / account / compartment) must be added into **3 different areas in Wiz**:

---

### **Step 1 – Add to Individual Line of Business (LOB) Grouping**

➡️ Place the account into the **appropriate LOB** folder.

**Example:**
`edp-prod-restrict-demmdi` (GCP project) → **Data & Analytics**

---

### **Step 2 – Add to CSP CVS & Affiliate Grouping**

➡️ Place the same account into the **CSP CVS or Affiliate grouping**, based on ownership.

* **CVS** → goes into the **CVS-specific grouping** for that cloud.
* **Affiliate** → goes into the **Affiliate grouping** for that cloud.

**Example:**
`edp-prod-restrict-demmdi` (CVS-owned GCP project) → **All-GCP-CVS-Subscriptions**

---

### **Step 3 – Add to CSP Grouping by Cloud**

➡️ Place the account into the **cloud provider grouping** (All\_AWS, All\_Azure, All\_GCP, All\_OCI).

**Example:**
`edp-prod-restrict-demmdi` (GCP project) → **All\_GCP**

---

✅ Every new account must be added in **all 3 steps above**.

---

Do you also want me to **expand this with a table template** (columns: *Account Name*, *LOB Grouping*, *CSP CVS/Affiliate*, *Cloud Grouping*) so the onboarding team can just fill it in for each new account?
