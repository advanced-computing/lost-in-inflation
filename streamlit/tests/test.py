from google.cloud import bigquery
import pandas as pd

bq_client = bigquery.Client()

df = bq_client.query("""
    SELECT Label, `PCE Inflation`
    FROM `sipa-adv-c-ibrahim-isaura.inflation_data.monthly_pce_inflation`
    ORDER BY Label
""").to_dataframe()

# Ensure datetime conversion
df["Label"] = pd.to_datetime(df["Label"], errors="coerce")

print(df["Label"].min(), df["Label"].max())
print(df["Label"].dt.month.value_counts())
