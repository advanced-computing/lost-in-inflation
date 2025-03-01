import os
import pytest
from my_streamlit_app import load_csv_data

# Get the absolute path of the `streamlit/` directory (where this script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This is `/home/runner/work/lost-in-inflation/lost-in-inflation/streamlit`
DATA_DIR = BASE_DIR  # Since CSV files are already in `streamlit/`

@pytest.fixture
def pce_df():
    csv_path = os.path.join(DATA_DIR, "MoM PCE.csv")
    return load_csv_data(csv_path, drop_cols=['Year', 'Month'], create_date_from=['Year', 'Month'])

@pytest.fixture
def china_mxp_df():
    csv_path = os.path.join(DATA_DIR, "EIUCOCHNTOT.csv")
    return load_csv_data(csv_path, period_col="Period", drop_cols=['Year', 'Period'], start_date="2018-01-01")

@pytest.fixture
def inflation_df():
    csv_path = os.path.join(DATA_DIR, "monthly-inflation-data.csv")
    return load_csv_data(csv_path, index_col="Label", date_col="Label")

def test_dataframes(pce_df, china_mxp_df, inflation_df):
    assert not pce_df.empty, "❌ PCE data is empty!"
    assert not china_mxp_df.empty, "❌ China MXP data is empty!"
    assert not inflation_df.empty, "❌ Inflation data is empty!"

    assert "Date" in pce_df.columns, "❌ PCE data is missing 'Date' column!"
    assert "Date" in china_mxp_df.columns, "❌ China MXP data is missing 'Date' column!"

    print("✅ All CSV data loaded correctly!")
