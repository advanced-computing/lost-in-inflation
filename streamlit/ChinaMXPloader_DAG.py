from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os

# =====================
# CONFIG
# =====================
PROJECT_ID = "sipa-adv-c-ibrahim-isaura"
DATASET_ID = "inflation_data"
TABLE_ID = "china_mxp"
CSV_FILE = "C:\repos\lost-in-inflation\streamlit\EIUCOCHNTOT.csv"  
CREDENTIALS_FILE = "C:\repos\lost-in-inflation\streamlit\sipa-adv-c-ibrahim-isaura-b600557db0a3.json"      

def load_china_mxp():
    print("🔄 Loading China MXP data via Airflow...")

    # --- Auth and client setup ---
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    dataset_ref = client.dataset(DATASET_ID)
    table_ref = dataset_ref.table(TABLE_ID)

    # --- Schema definition ---
    schema = [
        bigquery.SchemaField("Date", "DATE"),
        bigquery.SchemaField("ChinaMXP", "FLOAT"),
    ]

    # --- Ensure table exists ---
    try:
        client.get_table(table_ref)
    except Exception:
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"✅ Table {TABLE_ID} created.")

    # --- Load CSV and process ---
    df = pd.read_csv(CSV_FILE)
    df["Date"] = pd.to_datetime(df["Period"], errors="coerce").dt.date
    df = df[["Date", "ChinaMXP"]].dropna()

    # --- Load to BigQuery ---
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_APPEND",
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1
    )
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    print("✅ China MXP data loaded via Airflow.")

# =====================
# DAG Definition
# =====================
default_args = {
    "owner": "ibrahim",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "china_mxp_loader_dag",
    default_args=default_args,
    description="Load China MXP data into BigQuery",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["bigquery", "china", "inflation"]
)

load_china_mxp_task = PythonOperator(
    task_id="load_china_mxp",
    python_callable=load_china_mxp,
    dag=dag
)
