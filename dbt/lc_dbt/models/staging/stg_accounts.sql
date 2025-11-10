WITH raw AS (
    SELECT
        TRIM(accountid) AS account_id,
        CAST(customerid AS INTEGER) AS customer_id,
        CAST(balance AS DOUBLE) AS balance,
        LOWER(TRIM(accounttype)) AS account_type
    FROM read_csv_auto(
        '/app/dbt/lc_dbt/data/accounts.csv',
        header = TRUE,
        auto_detect = TRUE,
        normalize_names = TRUE,
        ignore_errors = TRUE
    )
),

dq AS (
    SELECT
        *,
        CASE WHEN account_id IS NOT NULL AND account_id != '' THEN 1 ELSE 0 END AS flag_account_id,
        CASE WHEN customer_id IS NOT NULL THEN 1 ELSE 0 END AS flag_customer_id,
        CASE WHEN balance IS NOT NULL AND balance >= 0 THEN 1 ELSE 0 END AS flag_balance,
        CASE WHEN account_type IN ('savings', 'checking') THEN 1 ELSE 0 END AS flag_account_type
    FROM raw
),

scored AS (
    SELECT
        *,
        ROUND((
            flag_account_id +
            flag_customer_id +
            flag_balance +
            flag_account_type
        ) / 4.0, 2) AS dq_score,
        CASE
            WHEN (
                (flag_account_id +
                 flag_customer_id +
                 flag_balance +
                 flag_account_type) / 4.0
            ) >= {{ var('dq_threshold') }}
            THEN 'pass'
            ELSE 'fail'
        END AS dq_status
    FROM dq
)

SELECT *
FROM scored
WHERE dq_status = 'pass'
