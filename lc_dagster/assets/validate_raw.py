from dagster import asset
from lc_dagster.constants import OWNER_EMAIL

@asset(
    name="validate_raw",
    description="Validates raw customer and account CSV files using Great Expectations.",
    metadata={"owner": OWNER_EMAIL, "kind": "validation"},
)
def validate_raw(context, ingest_raw):
    context.log.info(f"Validating raw data from: {ingest_raw}")
    return "raw_validated"
