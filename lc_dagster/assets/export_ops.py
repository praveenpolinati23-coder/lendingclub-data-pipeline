from dagster import asset, AssetObservation, MetadataValue
from lc_dagster.constants import DB_PATH, OUTPUT_DIR, OWNER_EMAIL
import duckdb
import os

@asset(
    name="export_results",
    description="Exports final interest calculation results from DuckDB to CSV and shows preview in Dagster UI.",
    metadata={"owner": OWNER_EMAIL, "kind": "export"},
)
def export_results(context, validate_output):
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Query the final results from DuckDB
    con = duckdb.connect(DB_PATH)
    df = con.execute("SELECT * FROM main_marts.fct_interest").fetchdf()
    con.close()

    # Write results to CSV
    output_path = os.path.join(OUTPUT_DIR, "account_summary.csv")
    df.to_csv(output_path, index=False)
    context.log.info(f"Exported results to {output_path}")

    # Emit metadata so it appears in Dagster UI
    context.add_output_metadata({
        "preview": MetadataValue.md(df.head().to_markdown()),  
        "path": MetadataValue.path(output_path),
        "rows": MetadataValue.int(len(df)),
    })

    # Emit event for lineage tracking
    context.log_event(
        AssetObservation(
            asset_key="export_results",
            metadata={"path": MetadataValue.path(output_path)},
        )
    )

    return output_path
