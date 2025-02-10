output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks_cluster.name
}

output "aks_cluster_id" {
  value = azurerm_kubernetes_cluster.aks_cluster.id
}

output "aks_managed_identity_object_id" {
  value = azurerm_kubernetes_cluster.aks_cluster.kubelet_identity[0].object_id
}
