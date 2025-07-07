Here’s a concise summary of **“finding,” “issue,” and “toxic combination”** based on the WhatsApp audio content:

---

### 🔍 **Finding**

* A **finding** is a *specific detection* of a **vulnerability** or **misconfiguration** on a **single resource**.
* Example types:

  * **Vulnerability Finding** – e.g., CVE on a VM.
  * **Cloud Configuration Finding** – e.g., public S3 bucket.
  * **Host Configuration Finding** – e.g., VM not logging failed login attempts.
* A single vulnerability on multiple resources = multiple findings.

---

### ⚠️ **Issue**

* An **issue** is a **toxic combination** of multiple risks across **different categories** (e.g., identity, network, storage).
* It reflects an *actual exploitable path* or *real security threat*.
* Example: A VM with a known CVE **and** access to a sensitive S3 bucket.

---

### ☣️ **Toxic Combination**

* A **toxic combination** is when:

  * Multiple low/medium risks combine (e.g., misconfigured network + exposed credential + access to data),
  * Resulting in a **real-world impact** like lateral movement, privilege escalation, or data exposure.
* Wiz policies and controls detect these combinations and generate **issues** from them.

---

### 🧠 **Why It Matters in Wiz**

* **Findings** give granularity,
* **Issues** give **contextualized, prioritized risks**,
* Helping avoid **alert fatigue** by showing what truly matters (i.e., what’s exploitable).

Let me know if you want a diagram or visual summary.
