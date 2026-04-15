Provision Azure Data Factory (ADF) and required dependent resources for the WIZ application in the Production environment (East US 2, rg-corp-use2-sa-prod). This includes ADF with private endpoint, SHIR VM for secure database connectivity, Key Vault for secret management, Storage Account for staging/pipeline data, and Azure Function App for integration logic.

The setup requires private networking (no public exposure), managed identities, and appropriate RBAC to enable secure communication between ADF, SHIR, PostgreSQL DB, Storage, Key Vault, and Function App.
