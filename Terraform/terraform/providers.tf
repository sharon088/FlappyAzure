terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.17.0"
    }
  }

  backend "azurerm" {
    resource_group_name   = "terraform-backend-rg"   #  Resource Group name
    storage_account_name  = "hdo3flappybirdstor"   #  Storage Account name
    container_name        = "tfstate"                 #  Blob Container name
    key                   = "terraform.tfstate"      # The name of the state file
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}
