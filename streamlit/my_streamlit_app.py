import streamlit as st
import pandas as pd
import json
import time
from google.cloud import bigquery
from google.oauth2 import service_account

import content as c
from charts import create_inflation_chart, create_pce_china_mxp_chart, create_decomposition_chart
from data_quality import run_quality_checks
from charts import run_pce_pca, plot_pca_loadings

# ======================
# Streamlit Setup
# ======================
st.set_page_config(page_title="Tariff-Inflation Analysis", layout="wide")
st.markdown("# 📈 **Tariff-Inflation Dashboard**")
st.caption("By Ibrahim & Isaura – Tracking real-time U.S. inflation shifts post-2025 tariff events.")

# ======================
# Optional Sidebar
# ======================
with st.sidebar:
    st.markdown("### 🇺🇸 Tariff Overview")
    st.markdown("This dashboard explores how newly announced tariffs affect U.S. inflation in real time.")
    st.markdown("- 📅 **Year**: 2025\n- 🧮 **Metric**: Cleveland Fed Nowcasting\n- 🌍 **Focus**: Trade Policy & Inflation")

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
    st.markdown("## 📄 Proposal")

    with st.container():
        st.markdown("#### 📊 What dataset are you going to use?")
        st.write(c.USED_DATASETS)

        st.markdown("#### ❓ What are your research question(s)?")
        st.write(c.RESEARCH_QUESTIONS)

        st.markdown("#### 🔗 Google Colab Link")
        st.write(c.GC_LINK)

        st.markdown("#### 🧭 Target Visualization")
        st.write(c.TARGET_VIS)

    with st.container():
        st.markdown("#### 🧩 Known Unknowns")
        st.warning(c.KNOWN_UNKNOWN)

        st.markdown("#### ⚙️ Anticipated Challenges")
        st.warning(c.CHALLENGES)

    st.markdown("## 📝 Updates")

    with st.container():
        st.markdown("#### 💡 Post-review Insights")
        st.info(c.INSIGHTS)

        st.markdown("#### 🔧 Post-review Adjustments")
        st.success(c.ADJUSTMENTS)
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
            excel_path = "streamlit/analysis_dataset.xlsx"
            st.plotly_chart(create_decomposition_chart(excel_path), use_container_width=True)

            # ========================
            # PCA: Variance Decomposition
            # ========================
            st.subheader("🧮 PCA: Variance Decomposition of Inflation Drivers")

            from charts import run_pce_pca, plot_pca_loadings

            xls = pd.ExcelFile(excel_path)
            drivers = {
                "gasoline_prices": "Energy",
                "average_hourly_earnings": "Services Proxy",
                "money_supply": "Money Supply",
                "consumer_sentiment": "Sentiment Proxy",
                "retail_and_services": "Headline PCE",
                "food_prices": "Food"
            }

            dfs = []

            for sheet, label in drivers.items():
                try:
                    df = xls.parse(sheet).dropna()
                    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]]) + pd.offsets.MonthEnd(0)
                    df = df[df[df.columns[0]] >= "2025-01-01"]
                    df = df.rename(columns={df.columns[0]: "Date"})

                    if sheet == "food_prices":
                        df["Food"] = df.iloc[:, 1:].pct_change().mean(axis=1)
                        df = df[["Date", "Food"]]
                    else:
                        if len(df.columns) > 1:
                            df[label] = df.iloc[:, 1].pct_change()
                            df = df[["Date", label]]
                        else:
                            st.warning(f"⚠️ Skipping {sheet} — not enough columns for {label}.")
                            continue

                    dfs.append(df)

                except Exception as e:
                    st.error(f"Error processing {sheet}: {e}")

            from functools import reduce
            pca_df = reduce(lambda left, right: pd.merge(left, right, on="Date", how="outer"), dfs).dropna()

            # Run PCA
            var_ratios, loadings, _ = run_pce_pca(pca_df)

            st.markdown(f"**Explained Variance:** PC1 = `{var_ratios[0]:.2%}`, PC2 = `{var_ratios[1]:.2%}`")
            st.caption(
                "🧠 *Food, Services, and Money Supply jointly explain most of the variation in inflation (PC1 ≈ 75%), "
                "while Energy behaves differently and drives a secondary pattern (PC2 ≈ 25%).*"
            )

            st.plotly_chart(plot_pca_loadings(loadings), use_container_width=True)

    else:
        st.warning("Data could not be loaded.")
