import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st

# Retrieve secrets from Streamlit's secrets management
PROJECT_ID = st.secrets["bigquery"]["project_id"]
PRIVATE_KEY = st.secrets["bigquery"]["private_key"]
CLIENT_EMAIL = st.secrets["bigquery"]["client_email"]
DATASET_ID = "inflation_data"
TABLE_ID = "monthly_pce_inflation"
CSV_FILE = "streamlit/monthly-inflation-data.csv"

# Authenticate using values from secrets.toml
credentials = service_account.Credentials.from_service_account_info({
    "type": "service_account",
    "project_id": PROJECT_ID,
    "private_key": PRIVATE_KEY,
    "client_email": CLIENT_EMAIL,
    "token_uri": "https://oauth2.googleapis.com/token"
})
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

# Define dataset/table reference
dataset_ref = client.dataset(DATASET_ID)
table_ref = dataset_ref.table(TABLE_ID)

# Define schema
schema = [
    bigquery.SchemaField("Label", "DATE"),
    bigquery.SchemaField("PCE Inflation", "FLOAT"),
    bigquery.SchemaField("Core PCE Inflation", "FLOAT"),
]

# Create table if it doesn't exist
try:
    client.get_table(table_ref)
except Exception:
    table = bigquery.Table(table_ref, schema=schema)
    client.create_table(table)
    print(f"Table {TABLE_ID} created.")

# Read CSV into DataFrame
df = pd.read_csv(CSV_FILE)
df["Label"] = pd.to_datetime(df["Label"]).dt.date

# Load data into BigQuery
job_config = bigquery.LoadJobConfig(
    schema=schema,
    write_disposition="WRITE_APPEND",
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1
)
job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
job.result()

print("Data successfully loaded into BigQuery.")

# Function to query data from BigQuery
def load_bigquery_data(query):
    # Reuse credentials/client to avoid reauthenticating
    query_client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    return query_client.query(query).to_dataframe()
