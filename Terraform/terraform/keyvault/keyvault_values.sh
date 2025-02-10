#!/bin/bash

# Get the Key Vault name from the argument passed to the script
VAULT_NAME=$1

# Set secrets in the Key Vault dynamically using the passed name
az keyvault secret set --vault-name "$VAULT_NAME" --name "AZURE-SQL-USERNAME" --value "adminuser"
az keyvault secret set --vault-name "$VAULT_NAME" --name "AZURE-SQL-PASSWORD" --value "Hdo3Flappy@!"
az keyvault secret set --vault-name "$VAULT_NAME" --name "AZURE-SQL-SERVER" --value "azmysql"
az keyvault secret set --vault-name "$VAULT_NAME" --name "AZURE-SQL-DATABASE" --value "azmydb"
