output "vnet_id" {
  value = azurerm_virtual_network.vnet.id
}

output "private_subnet_id" {
  value = azurerm_subnet.private_subnet.id
}

output "vnet_name" {
  value = azurerm_virtual_network.vnet.name
}
