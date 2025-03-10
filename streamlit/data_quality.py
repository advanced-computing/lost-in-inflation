import pandas as pd

def check_missing_values(df):
    """Check for missing values in the dataset."""
    missing_values = df.isnull().sum()
    if missing_values.any():
        print("Missing values detected:\n", missing_values[missing_values > 0])
    else:
        print("No missing values detected.")

def check_duplicates(df):
    """Check for duplicate rows in the dataset."""
    duplicate_rows = df.duplicated().sum()
    if duplicate_rows > 0:
        print(f"Warning: {duplicate_rows} duplicate rows found.")
    else:
        print("No duplicate rows detected.")

def check_date_column(df, column_name):
    """Check if the date column is in proper datetime format."""
    if column_name in df.columns:
        if not pd.api.types.is_datetime64_any_dtype(df[column_name]):
            print(f" Warning: {column_name} is not in datetime format. Converting now.")
            df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
            if df[column_name].isnull().any():
                print(f" Error: Some values in {column_name} could not be converted to datetime.")
    else:
        print(f" Error: {column_name} column not found in dataset.")

def check_expected_columns(df, expected_columns):
    """Ensure all expected columns are present in the dataset."""
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        print(f" Warning: Missing columns - {missing_columns}")
    else:
        print(" All expected columns are present.")

def check_outliers(df, numeric_columns):
    """Check for potential outliers using basic statistics (mean ± 3*std)."""
    for col in numeric_columns:
        if col in df.columns:
            mean = df[col].mean()
            std = df[col].std()
            outliers = df[(df[col] < mean - 3*std) | (df[col] > mean + 3*std)]
            if not outliers.empty:
                print(f" Warning: Potential outliers detected in {col}.")
            else:
                print(f" No significant outliers in {col}.")

def run_quality_checks(df, expected_columns, date_column=None, numeric_columns=[]):
    """Run all data quality checks on a dataset."""
    check_missing_values(df)
    check_duplicates(df)
    if date_column:
        check_date_column(df, date_column)
    check_expected_columns(df, expected_columns)
    check_outliers(df, numeric_columns)
