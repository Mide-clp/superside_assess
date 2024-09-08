output "database_name" {
  value = snowflake_database.superside.name
}

output "schema_name" {
  value = snowflake_schema.superside.name
}

output "airbyte_connection_id" {
  value = airbyte_connection.postgres_to_snowflake.connection_id
}