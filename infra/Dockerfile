# ===============================
# LendingClub Data Pipeline Dockerfile
# ===============================

FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*
COPY infra/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
ENV DAGSTER_HOME=/app/dagster_home
RUN mkdir -p $DAGSTER_HOME
RUN mkdir -p /app/dbt/lc_dbt/seeds /app/dbt/lc_dbt/models /app/dbt/lc_dbt/snapshots /app/dbt/lc_dbt/macros
RUN mkdir -p /root/.dbt && cp /app/dbt/lc_dbt/profiles.yml /root/.dbt/profiles.yml
RUN dbt deps --project-dir /app/dbt/lc_dbt --profiles-dir /app/dbt/lc_dbt || true
RUN chmod -R 777 /app
EXPOSE 3000
CMD ["dagster", "dev", "--host", "0.0.0.0", "--port", "3000"]
