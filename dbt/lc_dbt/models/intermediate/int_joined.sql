select
  a.account_id,
  a.customer_id,
  a.balance,
  a.account_type,
  c.name,
  c.has_loan
from {{ ref('stg_accounts') }} a
join {{ ref('stg_customers') }} c using(customer_id)
