# streamlit/daily_runner.py

from Gbqload import load_monthly_pce, load_china_mxp

if __name__ == "__main__":
    print("📥 Starting daily data pipeline...")
    load_monthly_pce()       # Scrapes Cleveland Fed + uploads PCE to BigQuery
    load_china_mxp()         # Optional: also uploads China MXP data from local CSV
    print("✅ Daily pipeline finished successfully.")