WITH source_date AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY date_day) AS date_id,
        *
    FROM {{ ref('src__date') }}

)

SELECT *
FROM
    source_date
