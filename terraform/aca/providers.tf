terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.72.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "insightnet-tfstate"
    storage_account_name = "tfstate0hnnf"
    container_name       = "insightnet-tfstate"
    key                  = "insightnet.tfstate"
  }
}

provider "azurerm" {
  features {}
}