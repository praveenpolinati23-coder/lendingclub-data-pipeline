from dagster import asset
from lc_dagster.constants import DATA_DIR, OWNER_EMAIL
import os

@asset(
    name="ingest_raw",
    description="Loads customer and account CSVs from the data directory.",
    metadata={
        "owner": OWNER_EMAIL,
        "kind": "ingestion",
        "automation": "manual",
    },
)
def ingest_raw(context):
    customers_path = os.path.join(DATA_DIR, "customers.csv")
    accounts_path = os.path.join(DATA_DIR, "accounts.csv")

    context.log.info(f"Found input files:\n{customers_path}\n{accounts_path}")
    return {"customers": customers_path, "accounts": accounts_path}
