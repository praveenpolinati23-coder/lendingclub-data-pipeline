from dagster import asset
from lc_dagster.constants import DB_PATH, OUTPUT_DIR, OWNER_EMAIL
import duckdb
import os

@asset(
    name="export_results",
    description="Exports final interest calculation results from DuckDB to CSV.",
    metadata={"owner": OWNER_EMAIL, "kind": "export"},
)
def export_results(context, validate_output):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    con = duckdb.connect(DB_PATH)
    df = con.execute("SELECT * FROM main_marts.fct_interest").fetchdf()
    output_path = os.path.join(OUTPUT_DIR, "final_interest.csv")
    df.to_csv(output_path, index=False)
    context.log.info(f" Exported results to {output_path}")
    return output_path
