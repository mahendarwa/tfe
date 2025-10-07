Here’s a **short and ready ServiceNow snippet version** 👇 — clean, brief, and still covers all required fields.

---

**Short Description:**
Delete obsolete GCS bucket `cvs-prisma-flow-logs` under GCP project `prisma-13368` (ITPM ID: apm0014613)

**Description:**
Project `prisma-13368` has been decommissioned. The associated GCS bucket `cvs-prisma-flow-logs` is no longer required. This change removes the unused bucket to ensure cost optimization and data hygiene.

**Justification:**
Bucket belongs to a decommissioned GCP project (Prisma). Safe to delete.

**Test Plan:**
Validate bucket no longer listed via `gsutil ls` after deletion.

**Risk & Impact:**
Low risk. Project inactive; no dependencies. No user impact.

**Communication Plan:**
Stakeholders notified — Satish (requester), Mahendar (executor). Update via Teams post-change.

**Implementation Plan:**

1. Confirm project access (`prisma-13368`)
2. Run deletion:
   `gsutil rm -r gs://cvs-prisma-flow-logs`
3. Validate via `gsutil ls`
4. Update ticket with confirmation
   *Duration:* ~30 mins

**Validation Plan:**
Ensure bucket removed in console and CLI. Notify Satish on completion.

**Backout Plan:**
Not applicable. Optional pre-deletion backup via `gsutil cp` if data exists.

**Schedule:**
Execute during 23:00–06:00 IST low-activity window.

---

Would you like me to make a **slightly more formal version** (for CAB approval) or keep it this short conversational format for internal low-risk change tickets?
