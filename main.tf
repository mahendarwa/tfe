
### Key Components and Resources in diagram architecture——

1. Resource Group:
   - Purpose: A logical container to manage and organize related Azure resources.
   - Why: All resources in the diagram are deployed within a specific resource group.

2. Virtual Network (VNet) and Subnets:
   - Purpose: Provides network isolation and security for resources.
   - Why: Ensures secure communication between resources and with external systems.

3. Azure Data Factory:
   - Purpose: Orchestrates data movement and transformation.
   - Why: Central component for ETL (Extract, Transform, Load) processes.

4. Storage Accounts:
   - Blob Storage / Data Lake Storage:
     - Purpose: Storage for raw and processed data.
     - Why: To store intermediate and final datasets used and produced by Data Factory pipelines.

5. Azure SQL Managed Instance (SQL MI):
   - Purpose: Relational database service for storing structured data.
   - Why: To store processed and transformed data for reporting and analytics.

6. API Gateway:
   - Purpose: Manage and secure API calls.
   - Why: To securely expose APIs used by various services and applications.

7. Logic Apps:
   - Purpose: Automate workflows and integrate apps, data, and services.
   - Why: To automate tasks and orchestrate processes triggered by time or events.

8. App Service:
   - Purpose: Host web applications.
   - Why: To host the front-end applications that interact with backend services and APIs.

9. Static Web Apps:
   - Purpose: Host static web content.
   - Why: To serve static content and provide a user interface for users.

10. Azure Key Vault:
    - Purpose: Manage secrets and keys securely.
    - Why: To store and manage sensitive information like API keys and database connection strings.

11. Azure Monitor:
    - Purpose: Monitor and manage Azure resources.
    - Why: To track the performance and health of the resources.

12. Azure Entra (Azure AD):
    - Purpose: Identity and access management.
    - Why: To manage user identities and control access to resources.


===========
Below is the code — creating individual	 resource.. you can create each in different file by creating .tf files




#### 1. Create the Resource Group

```hcl
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}
```

#### 2. Create Virtual Network and Subnets


resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "subnet1" {
  name                 = var.subnet1_name
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "subnet2" {
  name                 = var.subnet2_name
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/24"]
}
```

#### 3. Create Azure Data Factory

```hcl
resource "azurerm_data_factory" "data_factory" {
  name                = var.data_factory_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}
```

#### 4. Create Storage Accounts

```hcl
resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_account" "datalake" {
  name                     = var.datalake_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true
}
```

#### 5. Create Azure SQL Managed Instance

```hcl
resource "azurerm_sql_managed_instance" "sql_mi" {
  name                         = var.sql_mi_name
  location                     = azurerm_resource_group.rg.location
  resource_group_name          = azurerm_resource_group.rg.name
  administrator_login          = "sqladmin"
  administrator_login_password = "H@Sh1CoR3!"
  sku_name                     = "GP_Gen5_2"
  storage_size_in_gb           = 32
  vcores                       = 8
  subnet_id                    = azurerm_subnet.subnet1.id
}
```

#### 6. Create API Gateway

```hcl
resource "azurerm_api_management" "api_gateway" {
  name                = var.api_gateway_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  publisher_name = "example-publisher"
  publisher_email = "publisher@example.com"
  sku_name = "Developer_1"
}
```

#### 7. Create Logic Apps

```hcl
resource "azurerm_logic_app_workflow" "logic_app" {
  name                = var.logic_app_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}
```

#### 8. Create App Service

```hcl
resource "azurerm_app_service_plan" "app_service_plan" {
  name                = var.app_service_plan_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku {
    tier = "Standard"
    size = "S1"
  }
}

resource "azurerm_app_service" "app_service" {
  name                = var.app_service_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.app_service_plan.id
}
```

#### 9. Create Static Web Apps

```hcl
resource "azurerm_static_site" "static_site" {
  name                = var.static_site_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku {
    tier = "Free"
    size = "F1"
  }
}
```

#### 10. Create Azure Key Vault

```hcl
resource "azurerm_key_vault" "keyvault" {
  name                        = var.key_vault_name
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
}
```

#### 11. Set Up Monitoring (Azure Monitor)

```hcl
resource "azurerm_monitor_log_profile" "log_profile" {
  name = "example-log-profile"
  locations = ["global"]
  categories = ["Action", "Write", "Delete"]
  retention_policy {
    enabled = true
    days = 365
  }
}

resource "azurerm_monitor_metric_alert" "metric_alert" {
  name                = var.metric_alert_name
  resource_group_name = azurerm_resource_group.rg.name
  scopes              = [azurerm_data_factory.data_factory.id]
  criteria {
    metric_namespace = "Microsoft.DataFactory/factories"
    metric_name      = "ActivityRunsFailed"
    aggregation      = "Total"
    operator         = "GreaterThan"
    threshold        = 0
  }
  actions {
    action_group_id = azurerm_monitor_action_group.action_group.id
  }
}
```

#### 12. Configure Azure AD (Azure Entra)

```hcl
resource "azurerm_role_assignment" "ad_role_assignment" {
  principal_id   = data.azurerm_client_config.current.client_id
  role_definition_name = "Contributor"
  scope = azurerm_resource_group.rg.id
}
```

### Variables and Outputs

#### `variables.tf`

```hcl
variable "resource_group_name" {
  description = "The name of the resource group."
  default     = "example-resource-group"
}

variable "location" {
  description = "The Azure region to deploy resources."
  default     = "West US 2"
}

variable "vnet_name" {
  description = "The name of the virtual network."
  default     = "example-vnet"
}

variable "subnet1_name" {
  description = "The name of the first
