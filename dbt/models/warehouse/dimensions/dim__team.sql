WITH prep_dim_team AS (
    SELECT DISTINCT
        dim_team_id AS dim_id,
        team_id,
        team,
        team_type

    FROM
        {{ ref('stg__project') }}

)

SELECT *
FROM
    prep_dim_team
