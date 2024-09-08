WITH prep_dim_engagement_customer AS (
    SELECT DISTINCT
        dim_engagement_customer_id AS dim_id,
        customer_id,
        customer_name

    FROM
        {{ ref('stg__client_engagement') }}

)

SELECT *
FROM
    prep_dim_engagement_customer
