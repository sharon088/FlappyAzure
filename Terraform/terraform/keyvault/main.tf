data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {	
  name                = var.key_vault_name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku_name            = "standard"
  tenant_id           = data.azurerm_client_config.current.tenant_id

  soft_delete_retention_days = 7
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get", "Set", "List", "Delete"
    ]
  }

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = var.aks_managed_identity_object_id

    secret_permissions = [
      "Get"  // Grant AKS the 'Get' permission for secrets
    ]
  }

  provisioner "local-exec" {
    command = "bash ${path.module}/keyvault_values.sh ${azurerm_key_vault.kv.name}"
  }
}
