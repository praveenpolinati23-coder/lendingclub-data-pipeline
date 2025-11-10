WITH raw AS (
    SELECT
        CAST(customerid AS INTEGER) AS customer_id,
        LOWER(TRIM(_name)) AS name,
        CASE
            WHEN LOWER(TRIM(hasloan)) IN ('yes', 'y', 'true', '1') THEN 'yes'
            WHEN LOWER(TRIM(hasloan)) IN ('no', 'n', 'false', '0') THEN 'no'
            ELSE 'no'
        END AS has_loan
    FROM read_csv_auto(
        '/app/dbt/lc_dbt/data/customers.csv',
        header = TRUE,
        auto_detect = TRUE,
        normalize_names = TRUE
    )
),

dq AS (
    SELECT
        *,
        CASE WHEN customer_id IS NOT NULL THEN 1 ELSE 0 END AS flag_customer_id,
        CASE WHEN name IS NOT NULL AND name != '' THEN 1 ELSE 0 END AS flag_name,
        CASE WHEN has_loan IN ('yes', 'no') THEN 1 ELSE 0 END AS flag_has_loan
    FROM raw
),

scored AS (
    SELECT
        *,
        ROUND((
            flag_customer_id +
            flag_name +
            flag_has_loan
        ) / 3.0, 2) AS dq_score,
        CASE
            WHEN (
                (flag_customer_id +
                 flag_name +
                 flag_has_loan) / 3.0
            ) >= {{ var('dq_threshold') }}
            THEN 'pass'
            ELSE 'fail'
        END AS dq_status
    FROM dq
)

SELECT *
FROM scored
WHERE dq_status = 'pass'
