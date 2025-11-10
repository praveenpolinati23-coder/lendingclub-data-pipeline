# 💳 LendingClub Data Pipeline — End-to-End Data Engineering Project

## 📘 Overview

This project demonstrates a **modern, modular data pipeline** built for **LendingClub-like financial data**, designed to showcase **data engineering best practices** — ingestion, transformation, validation, and orchestration — all running locally in **Docker**.

It integrates:

* **Dagster** → orchestration and observability
* **dbt + DuckDB** → ELT transformations
* **Great Expectations (optional)** → DQ framework (removed for simplicity but extendable)
* **Docker Compose + Makefile** → reproducible runtime environment

The entire pipeline runs end-to-end with **one command** and produces a final output file `account_summary.csv`.

---

## 🚀 Features at a Glance

| Stage              | Technology       | Purpose                                              |
| :----------------- | :--------------- | :--------------------------------------------------- |
| **Ingestion**      | Python (Dagster) | Reads raw CSVs (`customers.csv`, `accounts.csv`)     |
| **Transformation** | dbt + DuckDB     | Cleans, joins, and calculates account-level interest |
| **Validation**     | dbt tests        | Column-level DQ checks and thresholds                |
| **Orchestration**  | Dagster          | End-to-end pipeline orchestration & monitoring       |
| **Export**         | DuckDB + Pandas  | Exports final output as `account_summary.csv`        |
| **Runtime**        | Docker           | Fully containerized runtime with Makefile automation |

---

## ⚙️ Prerequisites

Before you begin, ensure you have:

* **Docker Desktop** installed and running
* **Git** installed
* **Make** utility available (comes preinstalled on macOS/Linux)

No Python or dbt setup is needed locally — everything runs inside Docker.

---

## 🏗️ Setup & Execution

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/yourusername/lendingclub-data-pipeline.git
cd lendingclub-data-pipeline
```

---

### **2️⃣ Build the Docker Image**

```bash
make build
```

This command:

* Builds the Docker image from `infra/Dockerfile`
* Installs Python, Dagster, dbt, DuckDB, and dependencies
* Prepares internal folders (`dbt/lc_dbt`, `output`, `dagster_home`)

---

### **3️⃣ Run the Dagster UI**

```bash
make run
```

Then open your browser at 👉 [http://localhost:3000](http://localhost:3000)

You’ll see the **Dagster UI**, where you can visualize your entire data pipeline graphically.

---

### **4️⃣ View the Output**

After the pipeline completes successfully:

* The final CSV file appears at:

  ```
  output/account_summary.csv
  ```
* You can preview it directly in **Dagster UI → Assets → export_results**
* Or open it from your host machine inside the `output/` folder.

---

## 🧱 Folder Structure

```
lendingclub-data-pipeline/
│
├── Makefile                      → Root-level automation (build/run/clean)
│
├── infra/                        → Infrastructure & environment setup
│   ├── Dockerfile                → Builds Python + Dagster + dbt + DuckDB image
│   ├── docker-compose.yml        → Defines Dagster service & volume mounts
│   ├── requirements.txt          → Python dependencies
│
├── dbt/
│   └── lc_dbt/
│       ├── data/                 → Raw CSVs (customers.csv, accounts.csv)
│       ├── seeds/                → Reference lookups (e.g., interest rates)
│       ├── models/               → SQL transformations
│       │   ├── staging/          → Cleans raw input data
│       │   ├── intermediate/     → Joins, aggregates, computes KPIs
│       │   └── marts/            → Final models (e.g., fct_interest)
│       ├── snapshots/            → Historical tracking (SCD logic)
│       ├── dbt_project.yml       → dbt configuration
│       ├── profiles.yml          → DuckDB connection profile
│       ├── packages.yml          → External dbt utility packages
│       └── lc_dbt.duckdb         → DuckDB database file (auto-created)
│
├── lc_dagster/                   → Dagster orchestration
│   ├── assets/                   → Core pipeline logic
│   │   ├── ingest_assets.py      → Reads CSVs and prepares raw inputs
│   │   ├── validation_assets.py  → Performs schema & DQ validations
│   │   ├── dbt_assets.py         → Executes dbt (run, test, snapshot)
│   │   └── export_assets.py      → Exports final `account_summary.csv`
│   │
│   ├── jobs/                     → Dagster job definitions
│   │   └── interest_pipeline_job.py → Orchestrates all assets end-to-end
│   │
│   ├── constants.py              → Centralized paths (DBT, DuckDB, Output)
│   └── repository.py             → Registers all assets/jobs in Dagster repo
│
├── output/                       → Stores exported results
│   └── account_summary.csv       → ✅ Final output CSV file
│
└── README.md                     → Full documentation (this file)
```

---

## 🔄 Step-by-Step Pipeline Logic

| Step                     | File                   | Function            | Description                                                                     |
| ------------------------ | ---------------------- | ------------------- | ------------------------------------------------------------------------------- |
| **1. Ingest Raw Data**   | `ingest_assets.py`     | `ingest_raw()`      | Reads CSVs from `dbt/lc_dbt/data/` and validates structure                      |
| **2. Validate Raw Data** | `validation_assets.py` | `validate_raw()`    | Checks for missing values, incorrect types, etc.                                |
| **3. Run dbt Models**    | `dbt_assets.py`        | `run_dbt()`         | Executes dbt models (`staging → intermediate → marts`) and tests                |
| **4. Run Snapshots**     | `dbt_assets.py`        | `run_dbt()`         | Maintains history of changing account data                                      |
| **5. Validate Output**   | `validation_assets.py` | `validate_output()` | Ensures business rules and DQ thresholds met                                    |
| **6. Export Results**    | `export_assets.py`     | `export_results()`  | Writes final results to `output/account_summary.csv` and previews in Dagster UI |

---

## DBT Documentation & Lineage Visualization ##

* 🗂️ Explore Interactive dbt Docs (Data Lineage & Model Documentation)

Once the pipeline is running, you can generate and view dbt documentation inside Docker to explore the full data model lineage, schema, and tests.

🔧 Steps to Generate and Serve dbt Docs

1️⃣ Open a shell inside the running Dagster container

* docker exec -it lendingclub_dagster bash

💡 If the container isn’t running, start it first:

* make run

2️⃣ Navigate to the dbt project folder
* cd /app/dbt/lc_dbt
* dbt docs generate --profiles-dir /app/dbt/lc_dbt
* dbt docs serve --profiles-dir /app/dbt/lc_dbt --port 8080 --host 0.0.0.0

* Then open your browser → http://localhost:8080

## 📊 Key Concepts Covered

| Concept                           | Description                                                      |
| --------------------------------- | ---------------------------------------------------------------- |
| **Modular Orchestration**         | Each asset is independent, promoting testability and reusability |
| **DBT + DuckDB Integration**      | Local, lightweight ELT using SQL                                 |
| **Data Quality Validation**       | dbt tests enforce schema, null, and threshold checks             |
| **Containerized Runtime**         | Docker ensures reproducibility across machines                   |
| **Dagster Metadata**              | Rich UI visualization with logs, lineage, and asset status       |
| **Snapshots & Incremental Logic** | Tracks history of changing data points                           |

---

## 🧠 Design Decisions & Trade-offs

| Area                                        | Decision                                                   | Trade-off / Reasoning                            |
| ------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------ |
| **DuckDB**                                  | Chosen over PostgreSQL/Snowflake                           | Lightweight, file-based, ideal for local testing |
| **Dagster over Airflow**                    | Easier setup, great UI, strong local orchestration         | Not as mature for enterprise-scale DAGs          |
| **dbt Tests instead of Great Expectations** | Simpler integration with SQL-based checks                  | Lacks full profiling flexibility                 |
| **Single-thread dbt Execution**             | Ensures deterministic ordering & avoids concurrency issues | Slightly slower runtime                          |
| **Static Input CSVs**                       | Simulates realistic batch data                             | No streaming/real-time data yet                  |


---

## 🧩 Future Enhancements

| Category                 | Improvement                                       | Description                                          |
| ------------------------ | ------------------------------------------------- | ---------------------------------------------------- |
| **Data Quality**         | Reintroduce **Great Expectations**                | Richer validation & data scoring with thresholds     |
| **Scheduling**           | Add **Dagster sensors/schedules**                 | Automate daily or hourly pipeline runs               |
| **Machine Learning**     | Integrate a model for **loan default prediction** | Train ML model using intermediate tables as features |
| **Lineage & Governance** | Add **Atlan or OpenMetadata integration**         | Track dataset lineage and ownership automatically    |
| **Monitoring**           | Add **Prometheus + Grafana**                      | Dashboard for run history, latency, and DQ metrics   |
| **Cloud Migration**      | Move from DuckDB → Snowflake/BigQuery             | Enable scalability & multi-user collaboration        |
| **CI/CD**                | Add GitHub Actions workflow                       | Auto-build & test dbt/Dagster changes on PRs         |
| **Delta Snapshots**      | Incremental snapshotting                          | Store deltas instead of overwriting full data        |
| **Dynamic Inputs**       | S3 or API-based ingestion                         | Replace static CSVs with real upstream systems       |


---

## 💡 Why This Matters

This project mimics a **real-world data engineering pipeline** in a **reproducible local environment**, showing:

* Clear data lineage
* Testable transformations
* Automated orchestration
* Extensible architecture for ML and cloud migration
