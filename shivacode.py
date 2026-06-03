### 1. User / Azure AD Group (People Access)

* Used for **humans** who log in to Azure Portal.
* Example: Mahendar, Developers, Admins.
* Permissions are given through Azure AD Groups like `clgrp-aad-css-developer`.
* Makes access management easier—add/remove users from the group instead of assigning permissions individually.

**Layman Example:**

```text
Apartment Building
    ↓
Residents Group
    ↓
Access to Gym
```

If you join the Residents Group, you automatically get gym access.

---

### 2. Resource Group (RG)

* A logical container that holds related Azure resources.
* Example: Function App, Storage Account, Key Vault all placed in one RG.
* Permissions assigned at RG level automatically apply to all resources inside it.
* Easier than assigning permissions one by one.

**Layman Example:**

```text
House
 ├─ Bedroom
 ├─ Kitchen
 └─ Hall
```

Giving someone access to the **house** means they can access all rooms.

---

### 3. Role Assignment at RG Level

* Assign roles like Reader, Contributor, Website Contributor.
* One assignment covers all resources in that RG.
* New resources added later inherit the same access.
* Common for development teams.

**Layman Example:**

```text
Office Building Access Card
```

Instead of giving keys for every room, one card opens all rooms in that building.

---

### 4. System Assigned Managed Identity (Application Access)

* Identity created automatically for a single Azure resource.
* Commonly used by Function Apps, VMs, Logic Apps.
* Lets applications access Key Vault, Storage, SQL without passwords.
* Deleted automatically when the resource is deleted.

**Layman Example:**

```text
Company Printer
    ↓
Gets its own ID card
```

The printer can access the print server without anyone typing a password.

---

### 5. User Assigned Managed Identity (Shared Application Access)

* Created separately and can be attached to multiple resources.
* Same identity can be reused across Function Apps, VMs, Logic Apps.
* Permissions managed once and reused everywhere.
* Continues to exist even if one application is deleted.

**Layman Example:**

```text
Driver License
```

One driver license can be used to drive many cars.

---

### 6. Key Vault Secrets User

* Allows reading secrets from Key Vault.
* Cannot create, modify, or delete secrets.
* Commonly assigned to Function App Managed Identities.
* Used for API tokens, passwords, connection strings.

**Layman Example:**

```text
Locker Room Access
```

You can open and read your locker contents, but you cannot change the lock itself.

---

### 7. Your Current Scenario

**Human Access:**

```text
Mahendar
    ↓
clgrp-aad-css-developer
    ↓
Website Contributor
    ↓
rg-corp-use2-snap-prod
```

This lets developers manage the Function App.

**Application Access:**

```text
Function App
    ↓
System Managed Identity
    ↓
Key Vault Secrets User
    ↓
Key Vault
```

This lets the Function App read secrets securely.

---

### Easy Rule to Remember

```text
User / Group
    = Humans accessing Azure

System Managed Identity
    = One application accessing Azure resources

User Managed Identity
    = Many applications sharing one identity

Resource Group
    = Folder containing Azure resources

Role Assignment
    = Permission granted to a user/group/identity
```

**One-line memory trick:**

👉 **People use Azure AD Groups. Apps use Managed Identities. Resources live inside Resource Groups. Permissions are granted using Roles.**
