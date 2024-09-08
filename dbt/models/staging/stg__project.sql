WITH project_prep AS (

    SELECT
        *,
        {{ dbt_utils.generate_surrogate_key(["project_service_id", "service", "sub_service"]) }} AS dim_service_id,
        {{ dbt_utils.generate_surrogate_key(["product_id", "product"]) }}                        AS dim_product_id,
        {{ dbt_utils.generate_surrogate_key(["team", "team_type", "team_id"]) }}                 AS dim_team_id
    FROM
        {{ ref('project_seed') }}
)

SELECT *
FROM
    project_prep
