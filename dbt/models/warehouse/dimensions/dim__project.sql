WITH prep_dim_project AS (
    SELECT DISTINCT
        id AS dim_id,
        {{ dbt_utils.star(from=ref('stg__project'), except=["id", "project_service_id", "service","sub_service", "product_id", "product", "team_id", "team","team_type", "cpm", "cpm_id"]) }}

    FROM
        {{ ref('stg__project') }}

)

SELECT *
FROM
    prep_dim_project
