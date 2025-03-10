import pandas as pd

def load_csv_data(filepath, index_col=None, date_col=None, drop_cols=None, create_date_from=None, period_col=None, start_date=None):
    df = pd.read_csv(filepath)

    if create_date_from:
        df['Date'] = pd.to_datetime(df[create_date_from[0]].astype(str) + '-' + df[create_date_from[1]], format='%Y-%b')

    elif period_col:
        df['Month'] = df[period_col].str[1:].astype(int)
        df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%m')

    elif date_col:
        df[date_col] = pd.to_datetime(df[date_col])

    if drop_cols:
        df = df.drop(columns=drop_cols)

    if start_date:
        df = df[df['Date'] >= start_date]

    if index_col:
        df = df.set_index(index_col)

    return df
