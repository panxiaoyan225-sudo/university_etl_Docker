

   🎓 University Intelligence Framework & Automated ETL
This framework represents a technical implementation of a robust, automated data pipeline designed for high-reliability environments like government and higher education. It bridges the gap between architectural agility and statistical rigor through automated data quality (DQ) enforcement and containerized persistence.

🎯 Project Philosophy
Most analytics workflows suffer from manual data handling. This project demonstrates a high-performance, low-footprint architecture optimized for containerized environments. By moving from manual extracts to an automated Medallion Architecture, I achieved a scalable "Single Source of Truth" for university performance metrics while maintaining production-grade reliability.

🏗️ System Architecture
The framework orchestrates data through four specialized layers:

Ingestion Layer: Multi-protocol support for REST APIs (JSON) with built-in retry logic and exponential backoff to handle network instability.

Validation Layer (The Gatekeeper): A custom suite within transform.py that enforces schema integrity and logical consistency (e.g., non-null checks on university domains) before any database commits.

Persistence Layer (Bronze & Silver): * Bronze: Raw immutable JSON snapshots stored for auditability and lineage.

Silver: Structured relational storage using MySQL with optimized "Upsert" logic to prevent record duplication.

Audit & Logging: A centralized logging system (logging_config.py) that tracks row counts, API latency, and transformation errors in real-time.

🌊 The Pipelines
University Intelligence Pipeline: Consumes nested JSON from the Hipo Labs API, transforming nested lists into optimized, relational SQL tables ready for executive dashboards.

Automated Data Auditor: Monitors the ingestion process to ensure that only validated records regarding Canadian institutions reach the final persistence layer.

Medallion Snapshot System: Automatically versions raw data in the /data/bronze directory, ensuring historical data is preserved for longitudinal impact evaluations.

🛠️ Tech Stack
Languages: Python 3.11, SQL

Engineering: Docker, Docker Compose, SQLAlchemy, Apache Airflow

Data Science: Pandas (Vectorized transformations)

Environment: Cross-platform compatibility (Windows/Linux) via Containerization

📅 Apache Airflow – Scheduling & Monitoring
The pipeline is scheduled and monitored with Apache Airflow (LocalExecutor + PostgreSQL):

- **Airflow UI**: http://localhost:8080 — login: `admin` / `admin`
- **DAG**: `university_etl` runs daily (extract → transform → load); you can also trigger runs manually from the UI.
- **Services**: `postgres` (Airflow metadata), `airflow-init` (one-time DB init), `airflow-webserver`, `airflow-scheduler`. The ETL runs inside the scheduler when the DAG is triggered.

To run only the ETL container once (no Airflow), use the `manual` profile:

```powershell
docker compose --profile manual run --rm etl
```

🚀 Deployment Guide
To deploy this framework in a local or cloud environment:

Initialize Environment:

PowerShell
# Clone and enter directory
cd university_etl
Configure Secrets:

Rename .env.example to .env.

Ensure DB_HOST is set to mysql for internal Docker networking (Airflow services already use DB_HOST=mysql).

Launch via Docker (includes MySQL, Airflow, and scheduled ETL):

PowerShell
docker compose up --build

Wait for Airflow to be ready (scheduler + webserver), then open http://localhost:8080.

🚀 Project structure

university_etl/
  dags/
    university_etl_dag.py   # Airflow DAG (daily ETL)
  src/
    __init__.py
    main.py
    config.py
    logging_config.py
    db.py
    extract.py
    transform.py
    load.py
    models.py
  data/
    bronze/
      .gitkeep
  .env.example
  requirements.txt
  Dockerfile
  Dockerfile.airflow   # Airflow image with ETL deps + src
  docker-compose.yaml
  README.md   (optional but recommended)