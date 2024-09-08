WITH prep_dim_product AS (
    SELECT DISTINCT
        dim_product_id AS dim_id,
        product_id,
        product

    FROM
        {{ ref('stg__project') }}

)

SELECT *
FROM
    prep_dim_product
