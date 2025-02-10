data "azurerm_key_vault" "kv" {
  name                = var.key_vault_name
  resource_group_name = var.resource_group_name
}

# Fetch the SQL admin login from Key Vault
data "azurerm_key_vault_secret" "sql_admin_login" {
  name         = "AZURE-SQL-USERNAME"
  key_vault_id = data.azurerm_key_vault.kv.id
}

# Fetch the SQL admin password from Key Vault
data "azurerm_key_vault_secret" "sql_admin_password" {
  name         = "AZURE-SQL-PASSWORD"
  key_vault_id = data.azurerm_key_vault.kv.id
}

# Fetch the SQL server name from Key Vault
data "azurerm_key_vault_secret" "sql_server_name" {
  name         = "AZURE-SQL-SERVER"
  key_vault_id = data.azurerm_key_vault.kv.id
}

# Fetch the SQL database name from Key Vault
data "azurerm_key_vault_secret" "sql_database_name" {
  name         = "AZURE-SQL-DATABASE"
  key_vault_id = data.azurerm_key_vault.kv.id
}

resource "azurerm_mssql_server" "sql_server" {
  name                         = data.azurerm_key_vault_secret.sql_server_name.value
  resource_group_name          = var.resource_group_name
  location                     = var.location
  version                      = "12.0"
  administrator_login          = data.azurerm_key_vault_secret.sql_admin_login.value
  administrator_login_password = data.azurerm_key_vault_secret.sql_admin_password.value
}

resource "azurerm_mssql_database" "sql_database" {
  name           = data.azurerm_key_vault_secret.sql_database_name.value
  server_id      = azurerm_mssql_server.sql_server.id
  max_size_gb    = 2
  sku_name       = "S0"
}

resource "azurerm_mssql_virtual_network_rule" "aks_vnet_rule" {
  name                     = "aks-vnet-rule"
  server_id                = azurerm_mssql_server.sql_server.id
  subnet_id = var.vnet_subnet_id  
}

/*
resource "azurerm_mssql_firewall_rule" "aks_subnet_firewall" {
  name                = "allow-aks-subnet"
  server_id           = azurerm_mssql_server.sql_server.id
  
  # Use the passed subnet address prefix from the network module
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}
*/

