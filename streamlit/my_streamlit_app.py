import streamlit as st
import os
import time
import content as c
from helpers import load_csv_data
from charts import create_inflation_chart, create_pce_china_mxp_chart
from data_quality import run_quality_checks  # Import data quality checks

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.header("Tariff-Inflation Analysis")
st.subheader("Ibrahim & Isaura")
st.header("Proposal")
st.subheader("What dataset are you going to use?")
st.write(c.USED_DATASETS)
st.subheader("What are your research question(s)?")
st.write(c.RESEARCH_QUESTIONS)
st.subheader("Google Colab Link")
st.write(c.GC_LINK)
st.subheader("Target Visualization")
st.write(c.TARGET_VIS)
st.subheader("Known Unknowns")
st.write(c.KNOWN_UNKNOWN)
st.subheader("Anticipated Challenges")
st.write(c.CHALLENGES)
st.header("Updates")
st.subheader("Post-review Insights")
st.write(c.INSIGHTS)
st.subheader("Post-review Adjustments")
st.write(c.ADJUSTMENTS)


st.header("Analysis")

# Loading Data - now limited to PCE
@st.cache_data
def get_data():
    fed = load_csv_data(os.path.join(BASE_DIR, "monthly-inflation-data.csv"), index_col="Label", date_col="Label")

    # Keep only PCE & Core PCE, but leave china_mxp untouched
    pce_columns = ["PCE Inflation", "Core PCE Inflation"]
    if all(col in fed.columns for col in pce_columns):
        fed = fed[pce_columns]

    china_mxp = load_csv_data(
        os.path.join(BASE_DIR, "EIUCOCHNTOT.csv"),
        period_col="Period",
        drop_cols=['Year', 'Period'],
        start_date="2018-01-01"
    )

    pce = load_csv_data(
        os.path.join(BASE_DIR, "MoM PCE.csv"),
        drop_cols=['Year', 'Month'],
        create_date_from=['Year', 'Month']
    )

    # Run Data Quality Checks
    st.write("🔍 Running data quality checks...")
    run_quality_checks(fed, expected_columns=pce_columns, date_column="Label", numeric_columns=pce_columns)
    run_quality_checks(china_mxp, expected_columns=["Date", "ChinaMXP"], date_column="Date", numeric_columns=["ChinaMXP"])
    run_quality_checks(pce, expected_columns=["Date", "PCE"], date_column="Date", numeric_columns=["PCE"])

    return {"fed": fed, "china_mxp": china_mxp, "pce": pce}

# Load Data with Spinner
with st.spinner("Loading inflation data..."):
    data = get_data()
    time.sleep(1)  # Simulating delay

st.write("...Let's see what we got")

# Display Charts

st.write(c.INTRO_TEXT)
st.plotly_chart(create_inflation_chart(data["fed"]), use_container_width=True)

st.write(c.PCE_CHINA_TEXT)
st.plotly_chart(create_pce_china_mxp_chart(data["pce"], data["china_mxp"]), use_container_width=True)
