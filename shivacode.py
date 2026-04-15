Infra request template

Request Title:
Provision ADF and dependent resources for WIZ in Production

Subscription Name: Service Management Production
Subscription ID: 7f81ff32-74f5-45e3-bc03-a8141f72754d
Resource Group: rg-corp-use2-sa-prod
Region: East US 2
Environment: Prod
Application: WIZ

Objective

Provision Azure Data Factory and required dependent resources for the WIZ application in Production, using private connectivity and SHIR-based integration for secure communication with PostgreSQL, Blob Storage, Azure Function, and Key Vault.

Resources to be created
1) Azure Data Factory
Resource Type: Azure Data Factory
Suggested Name: adf-wiz-use2-prod
Purpose: Pipeline orchestration and integration
Requirements:
Private access / private endpoint
Managed identity enabled
Same subscription and resource group
2) SHIR VM
Resource Type: Virtual Machine for Self-Hosted Integration Runtime
Suggested Name: vm-wiz-shir-use2-prod
Purpose: Host SHIR for private/internal connectivity from ADF
Requirements:
Deploy in approved private subnet
Ready for SHIR installation
Internal connectivity to PostgreSQL and storage
Managed identity if applicable
3) Key Vault
Resource Type: Azure Key Vault
Suggested Name: kv-wiz-use2-prod
Purpose: Store secrets, credentials, connection strings
Requirements:
Prefer private access
Access for ADF and Function identities
4) Storage Account / Blob Storage
Resource Type: Azure Storage Account
Suggested Name: stwizuse2prod
Purpose: Staging, file exchange, pipeline storage
Requirements:
Blob service enabled
Private access if required
Access for ADF / SHIR / Function as needed
5) Azure Function App
Resource Type: Azure Function App
Suggested Name: func-wiz-use2-prod
Purpose: Application/integration logic invoked by ADF
Requirements:
HTTPS access
Managed identity enabled
Access to Key Vault and DB as required
Networking requirements

Configure private/internal communication for:

ADF → Azure Function on HTTPS 443
ADF → SHIR VM
SHIR VM → PostgreSQL DB on TCP 5432
ADF / SHIR / Function → Blob Storage
ADF / Function → Key Vault

Requirement: No unnecessary public exposure. ADF must be provisioned with private connectivity.
