WITH date_spine AS (
    {{
        dbt_utils.date_spine(
            datepart="day",
            start_date="to_date('11/01/2010', 'mm/dd/yyyy')",
            end_date="dateadd(year, 50, current_date)"
        )
    }}
),

calculated_date AS (
    SELECT
        date_day::DATE                 AS date_day,
        DATE_PART(DAYOFWEEK, date_day) AS day_of_the_week,
        DATE_PART(MONTH, date_day)     AS date_month,
        DATE_PART(YEAR, date_day)      AS date_year,
        DATE_PART(QUARTER, date_day)   AS date_quarter

    FROM date_spine
)

SELECT *
FROM
    calculated_date
