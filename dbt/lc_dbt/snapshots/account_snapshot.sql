{% snapshot account_snapshot %}
{{
    config(
        target_schema='snapshots',
        unique_key='account_id',
        strategy='timestamp',
        updated_at='last_updated'
    )
}}


SELECT
    account_id,
    customer_id,
    balance,
    account_type,
    CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS last_updated

FROM {{ ref('stg_accounts') }}

{% endsnapshot %}
