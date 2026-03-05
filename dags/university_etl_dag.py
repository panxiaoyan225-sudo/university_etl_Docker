"""
Apache Airflow DAG for the Hipo Labs University ETL pipeline.

Schedules and monitors: extract → transform → load into MySQL.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

# ETL runs in Airflow worker; ensure project root (parent of dags/) is on path
import sys
from pathlib import Path

_airflow_home = Path(__file__).resolve().parents[1]  # /opt/airflow
if str(_airflow_home) not in sys.path:
    sys.path.insert(0, str(_airflow_home))


def run_university_etl() -> None:
    """Run the full university ETL pipeline (extract → transform → load)."""
    from src.main import main
    main()


with DAG(
    dag_id="university_etl",
    description="Hipo Labs University ETL: extract from API, transform, load to MySQL",
    schedule_interval="@daily",  # Run once per day; use None for trigger-only
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["etl", "university", "hipo"],
) as dag:
    run_etl = PythonOperator(
        task_id="run_university_etl",
        python_callable=run_university_etl,
    )
