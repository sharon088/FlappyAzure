output "resource_group_name" {
  value = var.resource_group_name
}

output "aks_cluster_name" {
  value = module.aks.aks_cluster_name  # Output from the "aks" module
}