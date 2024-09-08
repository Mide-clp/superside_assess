WITH client_engagement_prep AS (

    SELECT
        *,
        {{ dbt_utils.generate_surrogate_key(["customer_id", "customer_name"]) }}                                   AS dim_engagement_customer_id,
        {{ dbt_utils.generate_surrogate_key(["service", "sub_service", "service_type", "detailed_sub_service"]) }} AS dim_engagement_service_id
    FROM {{ ref('src__client_engagement') }}
)

SELECT *
FROM
    client_engagement_prep
