from dagster import asset
from lc_dagster.constants import OWNER_EMAIL

@asset(
    name="validate_intermediate",
    description="Validates intermediate layer datasets.",
    metadata={"owner": OWNER_EMAIL, "kind": "validation"},
)
def validate_intermediate(context, validate_staging):
    context.log.info("Validating intermediate layer...")
    return "intermediate_validated"
