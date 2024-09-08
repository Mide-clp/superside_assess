resource "airbyte_source_postgres" "postgres" {
  configuration = {
    database    = var.postgres_database
    host        = var.postgres_host
    username    = var.postgres_username
    password    = var.postgres_password
    port        = var.postgres_port
    source_type = "postgres"
    schemas = [
      var.postgres_schema
    ]
    ssl_mode = {
      require = {

      }
    }
    tunnel_method = {
      no_tunnel = {

      }
    }
    replication_method = {
      scan_changes_with_user_defined_cursor = {

      }
    }
  }
  name         = "Postgres_public"
  workspace_id = var.airbyte_workspace_id
}


resource "airbyte_destination_snowflake" "snowflake" {
  configuration = {
    credentials = {
      username_and_password = {
          password = snowflake_user.third_party_user.password
      }
      
    }
    database         = snowflake_database.superside.name
    destination_type = "snowflake"
    host             = var.snowflake_host
    raw_data_schema  = snowflake_schema.superside.name
    role             = snowflake_database_role.third_party_role.name
    schema           = snowflake_schema.superside.name
    username         = snowflake_user.third_party_user.name
    warehouse        = snowflake_warehouse.superside.name
  }
  name         = "Snowflake_raw"
  workspace_id = var.airbyte_workspace_id
}

resource "airbyte_connection" "postgres_to_snowflake" {
  data_residency                       = "us"
  source_id                            = airbyte_source_postgres.postgres.source_id
  destination_id                       = airbyte_destination_snowflake.snowflake.destination_id
  name                                 = "employee_engagement_sync"
  namespace_definition                 = "destination"
  non_breaking_schema_updates_behavior = "propagate_columns"
  status                               = "active"
  configurations = {streams = [
    {
      name = "engagement_metrics"
      cursor_field = ["Load Date"]
      sync_mode = "incremental_append"
    }
  ]}
  schedule = {
    schedule_type = "manual"
  }
}