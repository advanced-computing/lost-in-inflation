import json
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Load secrets
with open(".streamlit/secrets.toml", "r") as f:
    lines = f.readlines()
secrets_dict = {}
for line in lines:
    if "=" in line:
        key, val = line.strip().split("=", 1)
        secrets_dict[key.strip()] = val.strip().strip('"')

project_id = secrets_dict["project_id"]
service_account_path = secrets_dict["service_account_file"]

credentials = service_account.Credentials.from_service_account_file(service_account_path)
client = bigquery.Client(credentials=credentials, project=project_id)

# Query to preview table columns
query = """
    SELECT *
    FROM `sipa-adv-c-ibrahim-isaura.inflation_data.monthly_pce_inflation`
    LIMIT 5
"""
df = client.query(query).to_dataframe()

print("\n🧾 BigQuery Table Columns:")
print(df.columns.tolist())
