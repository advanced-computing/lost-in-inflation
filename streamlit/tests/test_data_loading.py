import pytest
from my_streamlit_app import load_csv_data

@pytest.fixture
def test_pce():
    df = load_csv_data("./streamlit/MoM PCE.csv", drop_cols=['Year', 'Month'], create_date_from=['Year', 'Month'])
    return df

@pytest.fixture
def test_china_mxp():
    df = load_csv_data("./streamlit/EIUCOCHNTOT.csv", period_col="Period", drop_cols=['Year', 'Period'], start_date="2018-01-01")
    return df

@pytest.fixture
def test_df():
    df = load_csv_data("./streamlit/monthly-inflation-data.csv", index_col="Label", date_col="Label")
    return df

def test_dataframes(test_pce, test_china_mxp, test_df):
    assert not test_df.empty, "Fed inflation data (df) is empty!"
    assert not test_pce.empty, "PCE data is empty!"
    assert not test_china_mxp.empty, "China MXP data is empty!"

    assert "Date" in test_pce.columns, "PCE data is missing Date column!"
    assert "Date" in test_china_mxp.columns, "China MXP data is missing Date column!"

    print("✅ All CSV data loaded correctly!")