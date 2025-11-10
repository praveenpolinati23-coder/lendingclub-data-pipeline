from dagster import asset, AssetObservation, MetadataValue
from lc_dagster.constants import DBT_PROJECT_DIR, OWNER_EMAIL
import subprocess
import duckdb
import os

@asset(
    name="run_dbt",
    description="Runs dbt seed → run → snapshot and emits data quality scores.",
    metadata={"owner": OWNER_EMAIL, "kind": "transformation"},
)
def run_dbt(context, validate_intermediate):
    context.log.info("Installing dbt dependencies...")
    subprocess.run(
        ["dbt", "deps", "--project-dir", DBT_PROJECT_DIR, "--profiles-dir", DBT_PROJECT_DIR],
        check=True
    )

    context.log.info(" Seeding dbt data (lookup_interest_rate)...")
    subprocess.run(
        ["dbt", "seed", "--project-dir", DBT_PROJECT_DIR, "--profiles-dir", DBT_PROJECT_DIR],
        check=True
    )

    context.log.info(" Running dbt models...")
    subprocess.run(
        ["dbt", "run", "--project-dir", DBT_PROJECT_DIR, "--profiles-dir", DBT_PROJECT_DIR],
        check=True
    )

    context.log.info(" Running dbt snapshots...")
    subprocess.run(
        ["dbt", "snapshot", "--project-dir", DBT_PROJECT_DIR, "--profiles-dir", DBT_PROJECT_DIR],
        check=True
    )

    # Path to DuckDB database
    db_path = os.path.join(DBT_PROJECT_DIR, "lc_dbt.duckdb")

    # Fetch DQ metrics from dq_summary
    try:
        con = duckdb.connect(db_path)
        dq_query = """SELECT model, pass_rate FROM main_intermediate.dq_summary"""
        dq_results = con.execute(dq_query).fetchall()
        con.close()

        for model, pass_rate in dq_results:
            dq_status = "PASS " if pass_rate >= 0.8 else "FAIL "
            context.log.info(f"Model: {model}, Pass Rate: {pass_rate}, Status: {dq_status}")
            context.log_event(
                AssetObservation(
                    asset_key=f"dq_score_{model}",
                    metadata={
                        "model": MetadataValue.text(model),
                        "pass_rate": MetadataValue.float(pass_rate),
                        "status": MetadataValue.text(dq_status),
                    },
                )
            )
            if pass_rate < 0.8:
                raise Exception(f" Data Quality threshold not met for {model} (score={pass_rate})")

    except duckdb.CatalogException:
        context.log.warning("dq_summary table not found — skipping DQ score extraction.")
    except Exception as e:
        context.log.error(f"Error while fetching DQ metrics: {e}")
        raise

    return "dbt_run_complete"
