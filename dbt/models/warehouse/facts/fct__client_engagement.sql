{{
  config(
    materialized='incremental',
    unique_key=['dim_project_id', 'engagement_id', 'engagement_date']
    )
}}

WITH prep_incremental_client_engagement AS (
    SELECT *

    FROM {{ ref('stg__client_engagement') }}
    {% if is_incremental() %}

        WHERE
            airbyte_loaded_at
            >= (
                SELECT MAX(airbyte_loaded_at)
                FROM {{ this }} 
            )

    {% endif %}

),

client_engagement_with_project AS (
    SELECT
        prep_incremental_client_engagement.id,
        prep_incremental_client_engagement.engagement_id,
        dim_project.dim_id AS dim_project_id,
        prep_incremental_client_engagement.dim_engagement_customer_id,
        prep_incremental_client_engagement.dim_engagement_service_id,
        prep_incremental_client_engagement.engagement_date,
        prep_incremental_client_engagement.revenue,
        prep_incremental_client_engagement.revenue_usd,
        prep_incremental_client_engagement.engagement_type,
        prep_incremental_client_engagement.employee_count,
        prep_incremental_client_engagement.comments,
        prep_incremental_client_engagement.project_ref,
        prep_incremental_client_engagement.engagement_reference,
        prep_incremental_client_engagement.client_revenue,
        prep_incremental_client_engagement.revenue_currency,
        prep_incremental_client_engagement.client_revenue_currency,
        prep_incremental_client_engagement.source_loaded_at,
        prep_incremental_client_engagement.airbyte_loaded_at
    FROM
        prep_incremental_client_engagement
    RIGHT OUTER JOIN {{ ref("dim__project") }} AS dim_project ON prep_incremental_client_engagement.project_id = dim_project.project_id
)

SELECT *
FROM
    client_engagement_with_project
