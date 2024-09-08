########################################################
# Snowflake
########################################################
variable "snowflake_region" {
  type        = string
  description = "The region of the snowflake account"
  default     = "us-east-1"
}


variable "snowflake_account" {
  type        = string
  description = "The account of the snowflake account"
}

variable "snowflake_username" {
  type        = string
  description = "The username of the snowflake account"
}

variable "snowflake_password" {
  type        = string
  description = "The password of the snowflake account"
  sensitive   = true
}

variable "snowflake_role" {
  type        = string
  description = "The role of the user in the snowflake account"
  default     = "accountadmin"
}

variable "snowflake_host" {
  type        = string
  description = "The host of the snowflake account"
}

variable "third_party_user_password" {
  type        = string
  description = "The password of the third party user"
  sensitive   = true
}

variable "third_party_user_email" {
  type        = string
  description = "The email of the third party user"
}

########################################################
# Airbyte
########################################################
variable "airbyte_workspace_id" {
  type        = string
  description = "The workspace id of the airbyte account"
}

variable "airbyte_client_id" {
  type        = string
  description = "The client id of the airbyte account"
  sensitive   = true
}

variable "airbyte_client_secret" {
  type        = string
  description = "The client secret of the airbyte account"
  sensitive   = true
}

variable "api_key" {
  type        = string
  description = "The api key of the airbyte account"
  sensitive   = true
}

########################################################
# Postgres
########################################################
variable "postgres_database" {
  type        = string
  description = "The database of the postgres source"
}

variable "postgres_host" {
  type        = string
  description = "The host of the postgres source"
}

variable "postgres_username" {
  type        = string
  description = "The username of the postgres source"
}

variable "postgres_password" {
  type        = string
  description = "The password of the postgres source"
  sensitive   = true
}

variable "postgres_schema" {
  type        = string
  description = "The schema of the postgres source"
  default     = "public"
}

variable "postgres_port" {
  type        = number
  description = "The port of the postgres source"
  default     = 6543
}