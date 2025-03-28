import pandas as pd
import json
import time
from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st

# ======================
# Authentication
# ======================
PROJECT_ID = st.secrets["google_cloud"]["project_id"]
credentials_dict = json.loads(st.secrets["google_cloud"]["credentials"])
DATASET_ID = "inflation_data"

credentials = service_account.Credentials.from_service_account_info(credentials_dict)
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
dataset_ref = client.dataset(DATASET_ID)

# ======================
# 1. Load Monthly PCE Inflation Data
# ======================
start_time = time.time()

TABLE_ID_1 = "monthly_pce_inflation"
CSV_FILE_1 = "streamlit/monthly-inflation-data.csv"

schema1 = [
    bigquery.SchemaField("Label", "DATE"),
    bigquery.SchemaField("PCE Inflation", "FLOAT"),
    bigquery.SchemaField("Core PCE Inflation", "FLOAT"),
]

table_ref1 = dataset_ref.table(TABLE_ID_1)

# Create table if not exists
try:
    client.get_table(table_ref1)
except Exception:
    table1 = bigquery.Table(table_ref1, schema=schema1)
    client.create_table(table1)
    print(f"Table {TABLE_ID_1} created.")

# Read and load CSV
df1 = pd.read_csv(CSV_FILE_1)
df1["Label"] = pd.to_datetime(df1["Label"]).dt.date

job_config1 = bigquery.LoadJobConfig(
    schema=schema1,
    write_disposition="WRITE_APPEND",
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1
)
job1 = client.load_table_from_dataframe(df1, table_ref1, job_config=job_config1)
job1.result()

print(" Monthly PCE inflation data successfully loaded into BigQuery.")
end_time = time.time()
print(f"⏱ Load time for monthly PCE inflation: {end_time - start_time:.2f} seconds")

# ======================
# 2. Load China MXP Data
# ======================
start_time = time.time()

TABLE_ID_2 = "china_mxp"
CSV_FILE_2 = "streamlit/EIUCOCHNTOT.csv"

schema2 = [
    bigquery.SchemaField("Date", "DATE"),
    bigquery.SchemaField("ChinaMXP", "FLOAT"),
]

table_ref2 = dataset_ref.table(TABLE_ID_2)

# Read and format CSV
df2 = pd.read_csv(CSV_FILE_2)
df2["Date"] = pd.to_datetime(df2["Period"], errors="coerce").dt.date
df2 = df2[["Date", "ChinaMXP"]]
df2 = df2.dropna()

# Create table if not exists
try:
    client.get_table(table_ref2)
except Exception:
    table2 = bigquery.Table(table_ref2, schema=schema2)
    client.create_table(table2)
    print(f"Table {TABLE_ID_2} created.")

# Load to BigQuery
job_config2 = bigquery.LoadJobConfig(
    schema=schema2,
    write_disposition="WRITE_APPEND",
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1
)
job2 = client.load_table_from_dataframe(df2, table_ref2, job_config=job_config2)
job2.result()

print(" China MXP data successfully loaded into BigQuery.")
end_time = time.time()
print(f"⏱ Load time for China MXP: {end_time - start_time:.2f} seconds")

# ======================
# Query Function
# ======================
def load_bigquery_data(query):
    query_client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    return query_client.query(query).to_dataframe()
