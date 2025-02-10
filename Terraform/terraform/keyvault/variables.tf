variable "resource_group_name" {}
variable "location" {}
variable "key_vault_name" {}

variable "aks_managed_identity_object_id" {
  description = "The object ID of the AKS managed identity"
  type        = string
}

