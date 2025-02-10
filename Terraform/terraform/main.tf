module "resource_group" {
  source              = "./resource_group"
  resource_group_name = var.resource_group_name
  location            = var.location
}

module "keyvault" {
  source              = "./keyvault"
  resource_group_name = module.resource_group.resource_group_name
  location            = module.resource_group.location
  key_vault_name      = var.key_vault_name
  aks_managed_identity_object_id = module.aks.aks_managed_identity_object_id
}

module "acr" {
  source              = "./acr"
  resource_group_name = module.resource_group.resource_group_name
  location            = module.resource_group.location
  acr_name            = var.acr_name
  subnet_id           = module.network.private_subnet_id
}

module "network" {
  source              = "./network"
  resource_group_name = module.resource_group.resource_group_name
  location            = module.resource_group.location
}

module "aks" {
  source              = "./aks"
  resource_group_name = module.resource_group.resource_group_name
  location            = module.resource_group.location
  aks_cluster_name    = var.aks_cluster_name
  node_count          = var.node_count
  vnet_subnet_id      = module.network.private_subnet_id
  acr_id              = module.acr.acr_id
}

module "sql_server" {
  source              = "./sql_server"
  resource_group_name = module.resource_group.resource_group_name
  location            = module.resource_group.location
  key_vault_name      = module.keyvault.key_vault_name
  vnet_subnet_id      = module.network.private_subnet_id
  depends_on = [module.keyvault]
}


