from dagster import Definitions
from lc_dagster.assets.ingest_ops import ingest_raw
from lc_dagster.assets.validate_raw import validate_raw
from lc_dagster.assets.validate_staging import validate_staging
from lc_dagster.assets.validate_intermediate import validate_intermediate
from lc_dagster.assets.dbt_assets import run_dbt
from lc_dagster.assets.validate_output import validate_output
from lc_dagster.assets.export_ops import export_results
from lc_dagster.jobs.interest_pipeline import interest_pipeline

defs = Definitions(
    assets=[
        ingest_raw,
        validate_raw,
        validate_staging,
        validate_intermediate,
        run_dbt,
        validate_output,
        export_results,
    ],
    jobs=[interest_pipeline],
)
