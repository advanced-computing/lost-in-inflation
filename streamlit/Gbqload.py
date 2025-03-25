import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st

# Retrieve secrets from Streamlit's secrets management
PROJECT_ID = st.secrets["google_cloud"]["project_id"]
SERVICE_ACCOUNT_FILE = st.secrets["google_cloud"]["service_account_file"]
DATASET_ID = "inflation_data"
TABLE_ID = "monthly_pce_inflation"
CSV_FILE = "streamlit/monthly-inflation-data.csv"

# Authenticate with Google Cloud using the service account file from secrets
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

# Define dataset reference
dataset_ref = client.dataset(DATASET_ID)

# Define schema
schema = [
    bigquery.SchemaField("Label", "DATE"),
    bigquery.SchemaField("PCE Inflation", "FLOAT"),
    bigquery.SchemaField("Core PCE Inflation", "FLOAT"),
]

# Create table if it doesn't exist
table_ref = dataset_ref.table(TABLE_ID)
try:
    client.get_table(table_ref)  # Check if table exists
except Exception:
    table = bigquery.Table(table_ref, schema=schema)
    client.create_table(table)
    print(f"Table {TABLE_ID} created.")

# Read CSV into Pandas DataFrame
df = pd.read_csv(CSV_FILE)
df["Label"] = pd.to_datetime(df["Label"]).dt.date  # Ensure 'Label' column is in the correct date format

# Load data into BigQuery
job_config = bigquery.LoadJobConfig(
    schema=schema,
    write_disposition="WRITE_APPEND",  # Append new records
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1  # Skip header row
)

job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
job.result()  # Wait for the job to complete

print("Data successfully loaded into BigQuery.")
