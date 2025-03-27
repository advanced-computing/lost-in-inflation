import streamlit as st
import os
import time
import pandas as pd
import content as c
from Gbqload import load_bigquery_data
from helpers import load_csv_data
from charts import create_inflation_chart, create_pce_china_mxp_chart
from data_quality import run_quality_checks  # Import data quality checks

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="Tariff-Inflation Analysis", layout="wide")

st.title("Tariff-Inflation Analysis")
st.caption("By Ibrahim & Isaura")

# Create Tabs
tab1, tab2 = st.tabs(["📄 Proposal & Project Description", "📊 Analysis"])

# =======================
# Tab 1: Proposal
# =======================
with tab1:
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

# =======================
# Tab 2: Analysis
# =======================
with tab2:
    st.header("Analysis")

    @st.cache_data
    def get_data():
        pce_query = """
        SELECT Label, `PCE Inflation`, `Core PCE Inflation`
        FROM `sipa-adv-c-ibrahim-isaura.inflation_data.monthly_pce_inflation`
        """
        fed = load_csv_data(
            os.path.join(BASE_DIR, "monthly-inflation-data.csv"),
            drop_cols=[],
            date_col="Label"
        )

        # Convert Label to datetime (MM/DD/YYYY format is okay without format arg)
        fed["Label"] = pd.to_datetime(fed["Label"], errors="coerce")
        fed = fed.dropna(subset=["Label"])
        fed = fed.sort_values("Label")

        # Set the date as the index
        fed.set_index("Label", inplace=True)

        # Select only relevant columns
        pce_columns = ["PCE Inflation", "Core PCE Inflation"]
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

    with st.spinner("Loading inflation data..."):
        data = get_data()
        time.sleep(1)

    st.write("Let's see what we got")

    st.write(c.INTRO_TEXT)
    st.plotly_chart(create_inflation_chart(data["fed"]), use_container_width=True)

    st.write(c.PCE_CHINA_TEXT)
    st.plotly_chart(create_pce_china_mxp_chart(data["pce"], data["china_mxp"]), use_container_width=True)
