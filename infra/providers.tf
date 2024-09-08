terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "0.94.1"
    }

    airbyte = {
      source  = "airbytehq/airbyte"
      version = "0.4.1"
    }
  }
}

provider "snowflake" {
  # Configuration options
  account = var.snowflake_account
  // comment out the following variables to use pass the user and paassword as variables
    # user = var.snowflake_username
    # password = var.snowflake_password
  role = var.snowflake_role
}

provider "airbyte" {
  # Configuration options

  bearer_auth = var.api_key
#   client_id     = var.airbyte_client_id
#   client_secret = var.airbyte_client_secret
}