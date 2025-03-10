import streamlit as st
import os
import time
from helpers import load_csv_data
from charts import create_inflation_chart, create_pce_china_mxp_chart
from content import INTRO_TEXT, PCE_CHINA_TEXT  # Import text content

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# App Title
st.title("Lost-in-Inflation Team")
st.subheader("Team Members: Isaura Arias and Ibrahim Alangari")

# Loading Data
@st.cache_data
def get_data():
    return {
        "fed": load_csv_data(os.path.join(BASE_DIR, "monthly-inflation-data.csv"), index_col="Label", date_col="Label"),
        "china_mxp": load_csv_data(os.path.join(BASE_DIR, "EIUCOCHNTOT.csv"), period_col="Period", drop_cols=['Year', 'Period'], start_date="2018-01-01"),
        "pce": load_csv_data(os.path.join(BASE_DIR, "MoM PCE.csv"), drop_cols=['Year', 'Month'], create_date_from=['Year', 'Month'])
    }

# Load Data with Spinner
with st.spinner("Loading inflation data..."):
    data = get_data()
    time.sleep(1)  # Simulating delay

st.write("...Let's see what we got")

# Display Charts
st.plotly_chart(create_inflation_chart(data["fed"]), use_container_width=True)
st.write(INTRO_TEXT)  # Using imported text

st.plotly_chart(create_pce_china_mxp_chart(data["pce"], data["china_mxp"]), use_container_width=True)
st.write(PCE_CHINA_TEXT)  # Using imported text
