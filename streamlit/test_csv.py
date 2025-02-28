import pandas as pd
import pytest

def fix_and_validate_dates(df):
    """
    As our project receives datasets from different sources, this function is used to standardize the date format.
    Checks if all dates in the 'Date' column follow 'YYYY-MM-DD' format.
    Converts alternative formats to 'YYYY-MM-DD'.
    """
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.strftime('%Y-%m-%d')
    is_valid = not df["Date"].isna().any()
    return df, is_valid


# 1: Already Correct Format (YYYY-MM-DD)
#Used copilot to fix syntax 
def test_correct_format():
    df = pd.DataFrame({'Date': ['2025-02-21', '2024-06-15', '2023-12-31']})
    fixed_df, is_valid = fix_and_validate_dates(df)
    assert is_valid is True
    assert fixed_df["Date"].tolist() == ['2025-02-21', '2024-06-15', '2023-12-31']


# 2: Dates with Slashes (YYYY/MM/DD)
def test_slashes():
    df = pd.DataFrame({'Date': ['2025/02/21', '2024/06/15', '2023/12/31']})
    fixed_df, is_valid = fix_and_validate_dates(df)
    assert is_valid is True
    assert fixed_df["Date"].tolist() == ['2025-02-21', '2024-06-15', '2023-12-31']


# 3: Dates with Dashes in MM-DD-YYYY Format
def test_dashes_mm_dd_yyyy():
    df = pd.DataFrame({'Date': ['02-21-2025', '06-15-2024', '12-31-2023']})
    fixed_df, is_valid = fix_and_validate_dates(df)
    assert is_valid is True
    assert fixed_df["Date"].tolist() == ['2025-02-21', '2024-06-15', '2023-12-31']


# 4: Dates in DD-MM-YYYY Format
def test_dashes_dd_mm_yyyy():
    df = pd.DataFrame({'Date': ['21-02-2025', '15-06-2024', '31-12-2023']})
    fixed_df, is_valid = fix_and_validate_dates(df)
    assert is_valid is True
    assert fixed_df["Date"].tolist() == ['2025-02-21', '2024-06-15', '2023-12-31']


# 5: Invalid Dates
def test_invalid_dates():
    df = pd.DataFrame({'Date': ['2025-02-30', '2023-15-45', 'abc']})
    fixed_df, is_valid = fix_and_validate_dates(df)
    assert is_valid is False


# 6: Empty DataFrame
# Used copilot to fix syntax
def test_empty_dataframe():
    df = pd.DataFrame({'Date': []})
    fixed_df, is_valid = fix_and_validate_dates(df)
    assert is_valid is True  # No invalid data
    assert fixed_df.empty  # DataFrame should remain empty
