import streamlit as st
import os
import time
from helpers import load_csv_data
from charts import create_inflation_chart, create_pce_china_mxp_chart
from content import INTRO_TEXT, PCE_CHINA_TEXT
from data_quality import run_quality_checks  # Import data quality checks

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Loading Data - now limited to PCE
@st.cache_data
def get_data():
    fed = load_csv_data(os.path.join(BASE_DIR, "monthly-inflation-data.csv"), index_col="Label", date_col="Label")

    # Keep only PCE & Core PCE
    pce_columns = ["PCE", "Core PCE"]
    fed = fed[pce_columns] if all(col in fed.columns for col in pce_columns) else fed

    pce = load_csv_data(os.path.join(BASE_DIR, "MoM PCE.csv"), drop_cols=['Year', 'Month'], create_date_from=['Year', 'Month'])

    # Run Data Quality Checks
    st.write(" Running data quality checks...")
    run_quality_checks(fed, expected_columns=pce_columns, date_column="Label", numeric_columns=pce_columns)
    run_quality_checks(pce, expected_columns=["Date", "PCE"], date_column="Date", numeric_columns=["PCE"])

    return {"fed": fed, "pce": pce}

# Load Data with Spinner
with st.spinner("Loading inflation data..."):
    data = get_data()
    time.sleep(1)  # Simulating delay

st.write("...Let's see what we got")

# Display Charts
st.plotly_chart(create_inflation_chart(data["fed"]), use_container_width=True)
st.write(INTRO_TEXT)

st.plotly_chart(create_pce_china_mxp_chart(data["pce"], data["china_mxp"]), use_container_width=True)
st.write(PCE_CHINA_TEXT)
