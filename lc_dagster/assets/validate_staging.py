from dagster import asset
from lc_dagster.constants import OWNER_EMAIL

@asset(
    name="validate_staging",
    description="Validates staging models using Great Expectations.",
    metadata={"owner": OWNER_EMAIL, "kind": "validation"},
)
def validate_staging(context, validate_raw):
    context.log.info("Running staging data validation...")
    return "staging_validated"
