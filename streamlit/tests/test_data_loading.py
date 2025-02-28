import pytest
from my_streamlit_app import load_csv_data

@pytest.fixture
def pce_df():
    return load_csv_data("streamlit\MoM PCE.csv", drop_cols=['Year', 'Month'], create_date_from=['Year', 'Month'])

@pytest.fixture
def china_mxp_df():
    return load_csv_data("streamlit\EIUCOCHNTOT.csv", period_col="Period", drop_cols=['Year', 'Period'], start_date="2018-01-01")

@pytest.fixture
def inflation_df():
    return load_csv_data("streamlit\monthly-inflation-data.csv", index_col="Label", date_col="Label")

def test_dataframes(pce_df, china_mxp_df, inflation_df):
    assert not inflation_df.empty, "❌ Fed inflation data (df) is empty!"
    assert not pce_df.empty, "❌ PCE data is empty!"
    assert not china_mxp_df.empty, "❌ China MXP data is empty!"

    assert "Date" in pce_df.columns, "❌ PCE data is missing 'Date' column!"
    assert "Date" in china_mxp_df.columns, "❌ China MXP data is missing 'Date' column!"

    print("✅ All CSV data loaded correctly!")
