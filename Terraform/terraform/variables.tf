variable "resource_group_name" {
  description = "Name of the resource group."
  type        = string
}

variable "location" {
  description = "Azure region for the resources."
  type        = string
}

variable "acr_name" {
  description = "Azure Container registry name."
  type        = string
}

variable "aks_cluster_name" {
  description = "Name of the AKS cluster."
  type        = string
}

variable "node_count" {
  description = "Number of nodes in the default node pool."
  type        = number
  default     = 1
}


variable "key_vault_name" {
  description = "this is azure_key_vault"
  type        = string
}

