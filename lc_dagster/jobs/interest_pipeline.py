from dagster import job
from lc_dagster.assets import (
    ingest_raw,
    validate_raw,
    validate_staging,
    validate_intermediate,
    run_dbt,
    validate_output,
    export_results,
)

@job(name="interest_pipeline")
def interest_pipeline():
    export_results(
        validate_output(
            run_dbt(
                validate_intermediate(
                    validate_staging(
                        validate_raw(
                            ingest_raw()
                        )
                    )
                )
            )
        )
    )
