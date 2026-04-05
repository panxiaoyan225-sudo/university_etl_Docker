# University Intelligence Framework & Automated ETL
[📊 View ETL Infographic](https://panxiaoyan225-sudo.github.io/university_etl_Docker/university_infographic.html)

Technical implementations of a robust, automated data pipeline designed for high-reliability environments like government and higher education. This framework bridges the gap between architectural agility and statistical rigor through automated data quality (DQ) enforcement and containerized persistence.

## 🎯 Project Philosophy

Most analytics workflows suffer from manual data handling. This project demonstrates a **high-performance, low-footprint architecture** optimized for containerized environments. By moving from manual extracts to an automated Medallion Architecture, I achieved a scalable "Single Source of Truth" for university performance metrics while maintaining production-grade reliability.

## 🏗️ System Architecture

The framework orchestrates data through four specialized layers:

1.  **Ingestion Layer:** Multi-protocol support for REST APIs (JSON) with built-in retry logic and exponential backoff to handle network instability.
2.  **Validation Layer (The Gatekeeper):** A custom suite within `transform.py` that enforces schema integrity and logical consistency (e.g., non-null checks on university domains) before any database commits.
3.  **Persistence Layer (Bronze & Silver):**
    * **Bronze:** Raw immutable JSON snapshots stored for auditability and lineage.
    * **Silver:** Structured relational storage using MySQL with optimized "Upsert" logic to prevent record duplication.
4.  **Audit & Logging:** A centralized logging system (`logging_config.py`) that tracks row counts, API latency, and transformation errors in real-time.

## 🌊 The Pipelines

* **University Intelligence Pipeline:** Consumes nested JSON from the Hipo Labs API, transforming nested lists into optimized, relational SQL tables ready for executive dashboards.
* **Automated Data Auditor:** Monitors the ingestion process to ensure that only validated records regarding Canadian institutions reach the final persistence layer.
* **Medallion Snapshot System:** Automatically versions raw data in the `/data/bronze` directory, ensuring historical data is preserved for longitudinal impact evaluations.

## 🛠️ Tech Stack

* **Languages:** Python 3.11, SQL
* **Engineering:** Docker, Docker Compose, SQLAlchemy, Apache Airflow
* **Data Science:** Pandas (Vectorized transformations)
* **Environment:** Cross-platform compatibility (Windows/Linux) via Containerization

## 📅 Apache Airflow – Scheduling & Monitoring

The pipeline is scheduled and monitored with Apache Airflow (LocalExecutor + PostgreSQL):

* **Airflow UI:** `http://localhost:8080` — **Login:** `admin` / `admin`
* **DAG:** `university_etl` runs **@daily** (extract → transform → load); runs can also be triggered manually.
* **Services:** `postgres` (Metadata), `airflow-webserver`, `airflow-scheduler`, and `mysql`. The ETL runs inside the scheduler when triggered.

---

## 🚀 Deployment Guide

To deploy this framework in a local or cloud environment:

### 1. Initialize Environment
```powershell
# Clone and enter directory
cd university_etl