import pandas as pd
import time
import os
from datetime import datetime
from google.cloud import bigquery 
from helpers import download_current_month_csv  # ✅ import the scraper
from helpers import combine_clean_monthly_csvs
from auth import get_bigquery_credentials

# ======================
# Authentication
# ======================

credentials, PROJECT_ID = get_bigquery_credentials()
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
dataset_ref = client.dataset("inflation_data")

# ======================
# Load Monthly PCE Inflation Data
# ======================

def load_monthly_pce():
    print("🔄 Loading Monthly PCE Inflation...")
    start_time = time.time()

    TABLE_ID_1 = "monthly_pce_inflation"
    table_ref1 = dataset_ref.table(TABLE_ID_1)
    schema1 = [
        bigquery.SchemaField("Label", "DATE"),
        bigquery.SchemaField("PCE Inflation", "FLOAT"),
        bigquery.SchemaField("Core PCE Inflation", "FLOAT"),
    ]

    try:
        client.get_table(table_ref1)
    except Exception:
        table1 = bigquery.Table(table_ref1, schema=schema1)
        client.create_table(table1)
        print(f"✅ Table {TABLE_ID_1} created.")

    # Download raw modal CSV (with original column names)
    csv_path = download_current_month_csv(save_dir="streamlit/fed_data_per_month")
    if not csv_path or not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ Expected file not found: {csv_path}")
    df_raw = pd.read_csv(csv_path)

    # Reconstruct full date from MM/DD format in 'Label'
    now = datetime.now()
    df_raw["Label"] = pd.to_datetime(
        df_raw["Label"].apply(lambda x: f"{now.year}/{x}"),
        format="%Y/%m/%d",
        errors="coerce"
    )

    # Keep only rows for current month
    df_raw = df_raw[df_raw["Label"].dt.month == now.month]

    # Keep only relevant columns for BigQuery
    df_bq = df_raw[["Label", "PCE Inflation", "Core PCE Inflation"]].dropna()
    df_bq["Label"] = df_bq["Label"].dt.date  # Convert to DATE (not datetime)

    # Delete existing rows for the current month
    month_start = datetime(now.year, now.month, 1)
    if now.month == 12:
        month_end = datetime(now.year + 1, 1, 1)
    else:
        month_end = datetime(now.year, now.month + 1, 1)

    delete_query = f"""
        DELETE FROM `sipa-adv-c-ibrahim-isaura.inflation_data.{TABLE_ID_1}`
        WHERE Label >= DATE('{month_start.date()}') AND Label < DATE('{month_end.date()}')
    """
    client.query(delete_query).result()
    print(f"🧹 Truncated rows for {month_start.strftime('%B %Y')} in BigQuery")

    # Append new data for the current month
    job_config1 = bigquery.LoadJobConfig(
        schema=schema1,
        write_disposition="WRITE_APPEND",
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1
    )
    job1 = client.load_table_from_dataframe(df_bq, table_ref1, job_config=job_config1)
    job1.result()

    # Optional: regenerate local clean_monthly.csv for plotting
    combine_clean_monthly_csvs()

    print("✅ Monthly PCE inflation data loaded (incremental month update).")
    print(f"⏱ Load time: {time.time() - start_time:.2f} seconds")

# ======================
# Load China MXP Data
# ======================
def load_china_mxp():
    print("🔄 Loading China MXP Data...")
    start_time = time.time()

    TABLE_ID_2 = "china_mxp"
    CSV_FILE_2 = "streamlit/EIUCOCHNTOT.csv"
    schema2 = [
        bigquery.SchemaField("Date", "DATE"),
        bigquery.SchemaField("ChinaMXP", "FLOAT"),
    ]
    table_ref2 = dataset_ref.table(TABLE_ID_2)

    try:
        client.get_table(table_ref2)
    except Exception:
        table2 = bigquery.Table(table_ref2, schema=schema2)
        client.create_table(table2)
        print(f"✅ Table {TABLE_ID_2} created.")

    df2 = pd.read_csv(CSV_FILE_2)
    df2["Date"] = pd.to_datetime(df2["Date"], errors="coerce").dt.date
    df2 = df2[["Date", "ChinaMXP"]].dropna()

    job_config2 = bigquery.LoadJobConfig(
        schema=schema2,
        write_disposition="WRITE_APPEND",
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1
    )
    job2 = client.load_table_from_dataframe(df2, table_ref2, job_config=job_config2)
    job2.result()

    print("✅ China MXP data successfully loaded.")
    print(f"⏱ Load time: {time.time() - start_time:.2f} seconds")

# ======================
# Load MoM PCE Data
# ======================
def load_mom_pce():
    print("🔄 Loading MoM PCE Data...")
    start_time = time.time()

    TABLE_ID_3 = "mom_pce"
    CSV_FILE_3 = "streamlit/MoM PCE.csv"
    schema3 = [
        bigquery.SchemaField("Date", "DATE"),
        bigquery.SchemaField("PCE", "FLOAT"),
    ]
    table_ref3 = dataset_ref.table(TABLE_ID_3)

    try:
        client.get_table(table_ref3)
    except Exception:
        table3 = bigquery.Table(table_ref3, schema=schema3)
        client.create_table(table3)
        print(f"✅ Table {TABLE_ID_3} created.")

    df3 = pd.read_csv(CSV_FILE_3)
    df3["Date"] = pd.to_datetime(df3["Year"].astype(str) + "-" + df3["Month"].str.upper(), format="%Y-%b")
    df3["Date"] = df3["Date"].dt.date  # <- this ensures it's just a date, not datetime
    df3 = df3[["Date", "PCE"]].dropna()

    job_config3 = bigquery.LoadJobConfig(
        schema=schema3,
        write_disposition="WRITE_TRUNCATE",
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1
    )
    job3 = client.load_table_from_dataframe(df3, table_ref3, job_config=job_config3)
    job3.result()

    print("✅ MoM PCE data successfully loaded into BigQuery.")
    print(f"⏱ Load time: {time.time() - start_time:.2f} seconds")

# ======================
# Optional Query Function
# ======================
def load_bigquery_data(query):
    query_client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    return query_client.query(query).to_dataframe()

# ======================
# Main Execution Block
# ======================
if __name__ == "__main__":
    load_monthly_pce()
    load_china_mxp()
    load_mom_pce()
