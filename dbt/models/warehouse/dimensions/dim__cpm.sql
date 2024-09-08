WITH prep_dim_cpm AS (
    SELECT DISTINCT
        dim_cpm_id,
        cpm_id,
        cpm

    FROM
        {{ ref('stg__project') }}

)

SELECT *
FROM
    prep_dim_cpm
