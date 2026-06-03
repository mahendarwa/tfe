


==================
If you already have access to the Resource Group, you can grant access like this:
### Option 1: From Resource Group (recommended)
1. Go to **Resource Group**
   * `rg-corp-use2-snap-prod`
2. Click **Access Control (IAM)**
3. Click **+ Add** → **Add role assignment**
4. Search for:
   * **App Service Contributor** (recommended)
   * or **Website Contributor**
   * or **Contributor**
5. Select the role and click **Next**
6. Under **Members**, click **Select members**
7. Search:
   ```
   Mahendar.Sirarapu@CVSHealth.com
   ```
8. Select your account
9. Click **Review + Assign**
10. Wait 1-5 minutes and refresh Azure Portal.
---
### Option 2: From Function App Only
1. Open Function App:
   ```
   fa-corp-use2-snap-prod01
   ```
2. **Access Control (IAM)**
3. **Add Role Assignment**
4. Select **App Service Contributor**
5. Add your account
6. Review + Assign
---

### If "Add Role Assignment" is disabled
Then you don't have permission to grant roles.
Ask someone with:

* Owner
* User Access Administrator
* Privileged Role Administrator

to assign the role.
---
### Verify after assignment
Go to:
**Function App → Access Control (IAM) → Check Access**
Search your email.
You should see something like:
✅ App Service Contributor
or
✅ Contributor
Once assigned, refresh the Function App page and the Functions/App Settings should load.
