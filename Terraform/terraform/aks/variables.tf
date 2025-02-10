variable "resource_group_name" {
  type        = string
  description = "The name of the resource group"
}

variable "location" {
  type        = string
  description = "The Azure region to deploy the resources"
}

variable "aks_cluster_name" {
  type        = string
  description = "The name of the AKS cluster"
}

variable "node_count" {
  type        = number
  description = "The number of nodes in the AKS cluster"
}

variable "vnet_subnet_id" {
  description = "The ID of the subnet for AKS nodes"
  type        = string
}

variable "acr_id" {
  description = "The ID of the Azure Container Registry."
  type        = string
}

