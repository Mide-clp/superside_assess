WITH prep_dim_project_service AS (
    SELECT DISTINCT
        dim_service_id AS dim_id,
        project_service_id,
        service,
        sub_service

    FROM
        {{ ref('stg__project') }}

)

SELECT *
FROM
    prep_dim_project_service
