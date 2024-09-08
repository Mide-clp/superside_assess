WITH source AS (
    SELECT * FROM {{ source('landing_zone', 'engagement_metrics') }}
),

formatted_source AS (
    SELECT
        id::VARCHAR                        AS id,
        engagementid::VARCHAR              AS engagement_id,
        "PROJECT ID"::VARCHAR              AS project_id,
        "CUSTOMER ID"::INTEGER             AS customer_id,
        "CUSTOMER NAME"::VARCHAR           AS customer_name,
        "ENGAGEMENT DATE"::DATE            AS engagement_date,
        "REVENUE"::FLOAT                   AS revenue,
        "REVENUE USD"::FLOAT               AS revenue_usd,
        "SERVICE"::VARCHAR                 AS service,
        "SUB-SERVICE"::VARCHAR             AS sub_service,
        "ENGAGEMENT TYPE"::VARCHAR         AS engagement_type,
        "EMPLOYEE COUNT"::INTEGER          AS employee_count,
        "COMMENTS"::TEXT                   AS comments,
        "PROJECT REF"::VARCHAR             AS project_ref,
        "ENGAGEMENT REFERENCE"::VARCHAR    AS engagement_reference,
        "CLIENT REVENUE"::FLOAT            AS client_revenue,
        "SERVICE TYPE"::VARCHAR            AS service_type,
        "DETAILED SUB-SERVICE"::VARCHAR    AS detailed_sub_service,
        "REVENUE CURRENCY"::VARCHAR        AS revenue_currency,
        "CLIENT REVENUE CURRENCY"::VARCHAR AS client_revenue_currency,
        "LOAD DATE"::TIMESTAMP             AS source_loaded_at,
        "_AIRBYTE_EXTRACTED_AT"::TIMESTAMP AS airbyte_loaded_at

    FROM
        source
)


SELECT *
FROM
    formatted_source
