import streamlit as st
import pandas as pd
import json
import time
from google.cloud import bigquery
from google.oauth2 import service_account

import content as c
from charts import create_inflation_chart, create_pce_china_mxp_chart, create_decomposition_chart
from data_quality import run_quality_checks

# ======================
# Streamlit Setup
# ======================
st.set_page_config(page_title="Tariff-Inflation Analysis", layout="wide")
st.title("Tariff-Inflation Analysis")
st.caption("By Ibrahim & Isaura")

# ======================
# BigQuery Setup
# ======================
credentials_dict = json.loads(st.secrets["big_query"]["service_account_file"])
PROJECT_ID = st.secrets["big_query"]["project_id"]

credentials = service_account.Credentials.from_service_account_info(credentials_dict)
bq_client = bigquery.Client(credentials=credentials, project=PROJECT_ID)


# ======================
# Tabs
# ======================
tab1, tab2 = st.tabs(["📄 Proposal & Project Description", "📊 Analysis"])

# ======================
# Tab 1: Proposal
# ======================
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

# ======================
# Tab 2: Analysis
# ======================
with tab2:
    st.header("Analysis")

    @st.cache_data
    def get_data():
        try:
            # === Load Monthly PCE (Fed) data from BigQuery ===
            fed_query = """
                SELECT `Label`, `PCE Inflation`, `Core PCE Inflation`
                FROM `sipa-adv-c-ibrahim-isaura.inflation_data.monthly_pce_inflation`
                WHERE `Label` IS NOT NULL
                ORDER BY `Label`
            """
            fed = bq_client.query(fed_query).to_dataframe()
            fed["Label"] = pd.to_datetime(fed["Label"], errors="coerce")
            fed.set_index("Label", inplace=True)
            pce_columns = ["PCE Inflation", "Core PCE Inflation"]
            fed = fed[pce_columns]

            # === Load China MXP data ===
            china_query = """
                SELECT Date, ChinaMXP
                FROM `sipa-adv-c-ibrahim-isaura.inflation_data.china_mxp`
                WHERE Date IS NOT NULL AND ChinaMXP IS NOT NULL
                ORDER BY Date
            """
            china_mxp = bq_client.query(china_query).to_dataframe()
            china_mxp["Date"] = pd.to_datetime(china_mxp["Date"], errors="coerce")
            china_mxp = china_mxp[china_mxp["Date"].notna()]

            # === Load MoM PCE data ===
            pce_query = """
                SELECT Date, PCE
                FROM `sipa-adv-c-ibrahim-isaura.inflation_data.mom_pce`
                WHERE Date IS NOT NULL AND PCE IS NOT NULL
                ORDER BY Date
            """
            pce = bq_client.query(pce_query).to_dataframe()
            pce["Date"] = pd.to_datetime(pce["Date"], errors="coerce")
            pce = pce[pce["Date"].notna()]

            # === Run data quality checks
            st.write("🔍 Running data quality checks...")
            run_quality_checks(fed, expected_columns=pce_columns, date_column="Label", numeric_columns=pce_columns)
            run_quality_checks(china_mxp, expected_columns=["Date", "ChinaMXP"], date_column="Date", numeric_columns=["ChinaMXP"])
            run_quality_checks(pce, expected_columns=["Date", "PCE"], date_column="Date", numeric_columns=["PCE"])

            return {"fed": fed, "china_mxp": china_mxp, "pce": pce}

        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None

    with st.spinner("Loading inflation data..."):
        data = get_data()
        time.sleep(1)

    if data is not None:
        subtab1, subtab2 = st.tabs(["📉 PCE Inflation vs China MXP", "📊 MoM Core PCE & Decomposition"])

        with subtab1:
            st.subheader("PCE Inflation vs China MXP")
            st.write(c.PCE_CHINA_TEXT)
            st.plotly_chart(create_pce_china_mxp_chart(data["pce"], data["china_mxp"]), use_container_width=True)

        with subtab2:
            st.subheader("MoM Core PCE Inflation")
            st.write(c.INTRO_TEXT)
            st.plotly_chart(create_inflation_chart(data["fed"]), use_container_width=True)

            st.subheader("Inflation Decomposition (2025)")
            excel_path = "streamlit/analysis_dataset.xlsx"  # adjust as needed
            st.plotly_chart(create_decomposition_chart(excel_path), use_container_width=True)
    else:
        st.warning("Data could not be loaded.")

