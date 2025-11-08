with base as (
    select
        a.account_id,
        a.customer_id,
        a.balance,
        lower(a.account_type) as account_type,
        c.has_loan,
        r.base_rate,
        r.loan_bonus,

        case
            when lower(a.account_type) = 'savings' then
                r.base_rate + case when lower(c.has_loan) = 'yes' then r.loan_bonus else 0 end
            else 0
        end as interest_rate
    from {{ ref('int_joined') }} a
    join {{ ref('stg_customers') }} c
      on a.customer_id = c.customer_id
    join {{ ref('lookup_interest_rate') }} r
      on a.balance between r.range_min and r.range_max
)

select
    customer_id,
    account_id,
    balance as original_balance,
    interest_rate as interest_rate_applied,
    round(balance * interest_rate, 2) as annual_interest,
    round(balance + (balance * interest_rate), 2) as new_balance
from base
