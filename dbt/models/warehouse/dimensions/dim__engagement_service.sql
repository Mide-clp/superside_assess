WITH prep_dim_engagement_customer AS (
    SELECT DISTINCT
        dim_engagement_service_id AS dim_id,
        service,
        sub_service,
        service_type,
        detailed_sub_service

    FROM
        {{ ref('stg__client_engagement') }}

)

SELECT *
FROM
    prep_dim_engagement_customer
