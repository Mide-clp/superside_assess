resource "snowflake_warehouse" "superside" {
  name              = "SUPERSIDE_WAREHOUSE"
  comment           = "Data warehouse for SuperSide"
  warehouse_size    = "X-SMALL"
  auto_resume       = true
  auto_suspend      = 120
  min_cluster_count = 1
  max_cluster_count = 1
  warehouse_type    = "STANDARD"
}

resource "snowflake_database" "superside" {
  name                        = "SUPERSIDE"
  comment                     = "Database for SuperSide"
  data_retention_time_in_days = 1
}

resource "snowflake_schema" "superside" {
  database = snowflake_database.superside.name
  name     = "RAW"
  comment  = "Landing zone schema for SuperSide"
}

resource "snowflake_database_role" "third_party_role" {
  database = snowflake_database.superside.name
  name    = "integration_role"
  comment = "Role for thrid party to use to access the database"
}

resource "snowflake_user" "third_party_user" {
  depends_on   = [snowflake_warehouse.superside, snowflake_database.superside, snowflake_schema.superside, snowflake_database_role.third_party_role]
  name         = "superside_user"
  login_name   = "superside_user"
  comment      = "Third party user of the superside database."
  password     = var.third_party_user_password
  disabled     = false
  display_name = "SuperSide User"
  email        = var.third_party_user_email
  first_name   = "SuperSide"
  last_name    = "suser"

  default_warehouse = snowflake_warehouse.superside.name

  default_role         = snowflake_database_role.third_party_role.name
  must_change_password = false
}
