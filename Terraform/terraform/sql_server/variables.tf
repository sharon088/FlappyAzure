variable "resource_group_name" {}
variable "location" {}
variable "key_vault_name" {}

variable "vnet_subnet_id" {
  description = "The subnet ID of the AKS subnet"
  type        = string
}

