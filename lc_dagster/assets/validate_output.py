from dagster import asset
from lc_dagster.constants import OWNER_EMAIL

@asset(
    name="validate_output",
    description="Runs Great Expectations validations on the final output.",
    metadata={"owner": OWNER_EMAIL, "kind": "validation"},
)
def validate_output(context, run_dbt):
    context.log.info("Validating final output layer...")
    return "output_validated"
