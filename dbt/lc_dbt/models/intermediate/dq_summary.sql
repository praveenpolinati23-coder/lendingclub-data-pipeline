SELECT
    'stg_accounts' AS model,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN dq_status = 'pass' THEN 1 ELSE 0 END) AS passed,
    SUM(CASE WHEN dq_status = 'fail' THEN 1 ELSE 0 END) AS failed,
    ROUND(SUM(CASE WHEN dq_status = 'pass' THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 2) AS pass_rate
FROM {{ ref('stg_accounts') }}
UNION ALL
SELECT
    'stg_customers',
    COUNT(*),
    SUM(CASE WHEN dq_status = 'pass' THEN 1 ELSE 0 END),
    SUM(CASE WHEN dq_status = 'fail' THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN dq_status = 'pass' THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 2)
FROM {{ ref('stg_customers') }}
