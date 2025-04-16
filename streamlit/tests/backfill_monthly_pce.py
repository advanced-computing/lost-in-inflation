import os
import pandas as pd
from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client()
dataset_ref = client.dataset("inflation_data")

# Quick check on table contents
query = """
    SELECT Label, `PCE Inflation`
    FROM `sipa-adv-c-ibrahim-isaura.inflation_data.monthly_pce_inflation`
    ORDER BY Label
"""
df_check = client.query(query).to_dataframe()
df_check["Label"] = pd.to_datetime(df_check["Label"], errors="coerce")  
print(df_check["Label"].min(), df_check["Label"].max())
print(df_check["Label"].dt.month.value_counts())
print(df_check.tail())

def backfill_previous_months():
    print("📦 Backfilling Jan–Mar 2025 into BigQuery...")

    months = ["2025-1.csv", "2025-2.csv", "2025-3.csv"]
    schema = [
        bigquery.SchemaField("Label", "DATE"),
        bigquery.SchemaField("PCE Inflation", "FLOAT"),
        bigquery.SchemaField("Core PCE Inflation", "FLOAT"),
    ]

    for filename in months:
        file_path = os.path.join("streamlit/fed_data_per_month", filename)
        if not os.path.exists(file_path):
            print(f"❌ {filename} not found.")
            continue

        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()


        # Construct full date from MM/DD format
        df["Label"] = pd.to_datetime(
            "2025/" + df["Label"].astype(str),
            format="%Y/%m/%d",
            errors="coerce"
        )
        # Drop rows with invalid dates or missing inflation data
        df = df[["Label", "PCE Inflation", "Core PCE Inflation"]].dropna()
        df["Label"] = df["Label"].dt.date

        print(f"🧪 Preview of parsed dates from {filename}:")
        print(df["Label"].dropna().unique()[:3])

        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",
            schema=schema
        )

        client.load_table_from_dataframe(
            df, dataset_ref.table("monthly_pce_inflation"), job_config=job_config
        ).result()

        print(f"✅ Uploaded: {filename}")

if __name__ == "__main__":
    backfill_previous_months()
