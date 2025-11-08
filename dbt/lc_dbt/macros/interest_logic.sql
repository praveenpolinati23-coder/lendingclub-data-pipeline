{% macro calculate_interest(balance, has_loan, account_type) %}
(
  case
    when lower({{ account_type }}) = 'savings' then
      case
        when {{ balance }} < 10000 then 0.01
        when {{ balance }} between 10000 and 20000 then 0.015
        else 0.02
      end
    else 0
  end
  + case when lower({{ has_loan }}) = 'yes' and lower({{ account_type }}) = 'savings' then 0.005 else 0 end
)
{% endmacro %}
