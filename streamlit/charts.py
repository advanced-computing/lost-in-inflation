import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def create_inflation_chart(df):
    """Creates a Plotly chart for PCE and Core PCE inflation data with major 2025 tariff events."""
    fig = go.Figure()

    # Plot each inflation series
    for col in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[col],
            mode='lines+markers',
            name=col,
            connectgaps=False
        ))

    # Tariff event dates with labels
    tariff_events = [
        {"date": datetime(2025, 2, 1), "label": "Tariffs Announced<br>Canada, Mexico, China"},
        {"date": datetime(2025, 2, 10), "label": "Tariffs on Steel & Aluminum"},
        {"date": datetime(2025, 3, 4), "label": "Tariffs Implemented<br>Canada, Mexico, China"},
        {"date": datetime(2025, 4, 2), "label": "Liberation Day Tariffs"},
        {"date": datetime(2025, 4, 10), "label": "Tariffs on China<br>raised to 145%"},
    ]

    # Predefined y-positions to stagger annotation text
    y_positions = [1.05, 0.9, 1.0, 0.85, 0.95]

    # Add vertical lines and annotations
    for i, event in enumerate(tariff_events):
        y_pos = y_positions[i % len(y_positions)]  # Loop through y_positions if needed

        # Vertical dashed line
        fig.add_shape(
            type="line",
            x0=event["date"],
            x1=event["date"],
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(color="red", width=1, dash="dash")
        )

        # Text annotation
        fig.add_annotation(
            x=event["date"],
            y=y_pos,
            xref="x",
            yref="paper",
            text=f"{event['label']}<br>({event['date'].strftime('%Y-%m-%d')})",
            showarrow=False,
            font=dict(color="red", size=11),
            align="left"
        )

    # Layout
    fig.update_layout(
        title="Inflation Rate with 2025 Tariff Events",
        xaxis_title="Date",
        yaxis_title="Inflation Rate (%)",
        legend_title="Inflation Metrics",
        width=1200,
        height=600,
        template="plotly_white"
    )

    return fig

def create_pce_china_mxp_chart(pce, china_mxp):
    if "PCE" not in pce.columns or "Date" not in pce.columns:
        raise ValueError("Missing PCE or Date column in PCE dataframe.")
    if "ChinaMXP" not in china_mxp.columns or "Date" not in china_mxp.columns:
        raise ValueError("Missing ChinaMXP or Date column in China MXP dataframe.")

    # Ensure Date columns are datetime
    pce["Date"] = pd.to_datetime(pce["Date"], errors="coerce")
    china_mxp["Date"] = pd.to_datetime(china_mxp["Date"], errors="coerce")

    # Drop NaNs in value columns
    pce = pce.dropna(subset=["PCE"])
    china_mxp = china_mxp.dropna(subset=["ChinaMXP"])

    # Inner join for aligned plotting
    merged = pd.merge(pce, china_mxp, on="Date", how="inner")

    fig = go.Figure()

    # PCE (left y-axis)
    fig.add_trace(go.Scatter(
        x=merged["Date"],
        y=merged["PCE"],
        name="PCE Inflation",
        yaxis="y1",
        mode="lines+markers"
    ))

    # China MXP (right y-axis)
    fig.add_trace(go.Scatter(
        x=merged["Date"],
        y=merged["ChinaMXP"],
        name="China MXP",
        yaxis="y2",
        mode="lines+markers"
    ))

    # Tariff event markers
    tariff_events = [
        {"date": datetime(2018, 3, 22), "label": "Tariff Announced"},
        {"date": datetime(2018, 7, 6), "label": "Round 1 Tariffs"},
        {"date": datetime(2018, 9, 24), "label": "Round 3 Tariffs"},
        {"date": datetime(2019, 5, 10), "label": "$200B Raised to 25%"},
        {"date": datetime(2020, 1, 15), "label": "Phase One Deal"},
        {"date": datetime(2021, 6, 9), "label": "Biden Keeps China Tariffs"},
    ]

    for event in tariff_events:
        fig.add_shape(
            type="line",
            x0=event["date"], x1=event["date"],
            y0=0, y1=1,
            xref="x", yref="paper",
            line=dict(color="red", width=1, dash="dash")
        )
        fig.add_annotation(
            x=event["date"],
            y=1,
            xref="x",
            yref="paper",
            text=f"{event['label']}<br>({event['date'].strftime('%Y-%m-%d')})",
            showarrow=False,
            font=dict(color="red", size=10),
            align="left",
            xanchor="left",
            yanchor="bottom"
        )

    fig.update_layout(
        title="PCE Inflation vs. China MXP",
        xaxis_title="Date",
        yaxis=dict(title="PCE Inflation", side="left"),
        yaxis2=dict(
            title="China MXP",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        width=1200,
        height=600,
        legend=dict(x=0.01, y=0.99)
    )

    return fig
def create_decomposition_chart(filepath: str):
    xls = pd.ExcelFile(filepath)

    # Define sheets with grouping
    sheet_config = {
        "gasoline_prices": ("Energy", "pct_change"),
        "average_hourly_earnings": ("Services Proxy", "pct_change"),
        "money_supply": ("Money Supply", "pct_change"),
        "consumer_sentiment": ("Sentiment Proxy", "pct_change"),
        "retail_and_services": ("Headline PCE", "pct_change"),  # now labeled correctly
        "food_prices": {
            "Meat": "Food",
            "Dairy": "Food",
            "Cereals": "Food",
            "Oils": "Food",
            "Sugar": "Food"
        }
    }

    combined = pd.DataFrame()

    # Helper to load and process each individual sheet
    def process_sheet(sheet_name, col_mapping, group_name=None):
        df = xls.parse(sheet_name).dropna()
        df[df.columns[0]] = pd.to_datetime(df[df.columns[0]]) + MonthEnd(0)
        df = df[df[df.columns[0]] >= "2025-01-01"]
        df = df.rename(columns={df.columns[0]: "Date"})

        if isinstance(col_mapping, dict):  # multi-column food_prices
            dfs = []
            for original_col, new_group in col_mapping.items():
                sub_df = df[["Date", original_col]].copy()
                sub_df[original_col] = sub_df[original_col].pct_change()
                sub_df = sub_df.rename(columns={original_col: "Value"})
                sub_df["Category"] = new_group
                dfs.append(sub_df)
            return pd.concat(dfs)
        else:
            series = df[["Date", df.columns[1]]].copy()
            series[df.columns[1]] = series[df.columns[1]].pct_change()
            series = series.rename(columns={df.columns[1]: "Value"})
            series["Category"] = group_name
            return series.dropna()

    processed_dfs = []

    for sheet, config in sheet_config.items():
        if isinstance(config, tuple):
            group_label, method = config
            processed_dfs.append(process_sheet(sheet, sheet_config[sheet][0], group_label))
        elif isinstance(config, dict):
            processed_dfs.append(process_sheet(sheet, config))

    # Combine and aggregate categories
    long_df = pd.concat(processed_dfs).dropna()
    agg_df = long_df.groupby(["Date", "Category"]).sum().reset_index()

    # Pivot for stacking
    pivot = agg_df.pivot(index="Date", columns="Category", values="Value").fillna(0)
    pivot["Headline PCE"] = pivot["Headline PCE"]  # retain line before dropping from stack
    bar_categories = pivot.drop(columns=["Headline PCE"]).columns

    # Create figure
    fig = go.Figure()

    # Add stacked bars
    for cat in bar_categories:
        fig.add_trace(go.Bar(
            x=pivot.index,
            y=pivot[cat],
            name=cat
        ))

    # Add Headline PCE line
    fig.add_trace(go.Scatter(
        x=pivot.index,
        y=pivot["Headline PCE"],
        mode="lines+markers",
        name="Headline PCE (MoM)",
        line=dict(color="black", width=2),
        showlegend=True
    ))

    # Final layout
    fig.update_layout(
        title="Headline PCE Decomposition (MoM % Change)",
        barmode="relative",
        xaxis_title="Date",
        yaxis_title="Contribution to MoM Headline Inflation (%)",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig

def run_pce_pca(df: pd.DataFrame):
    features = ['Energy', 'Food', 'Money Supply', 'Sentiment Proxy']
    X = df[features].dropna()
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # Explained variance
    variance_ratios = pca.explained_variance_ratio_

    # Component loadings
    loadings = pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2'], index=features)

    return variance_ratios, loadings, X_pca

def plot_pca_loadings(loadings):
    category_colors = {
        "Energy": "#636EFA",
        "Food": "#EF553B",
        "Money Supply": "#00CC96",
        "Services Proxy": "#AB63FA",
        "Earnings Proxy": "#AB63FA",
        "Sentiment Proxy": "#AB63FA"  
    }

    fig = go.Figure()
    for pc in loadings.columns:
        fig.add_trace(go.Bar(
            x=loadings.index,
            y=loadings[pc],
            name=pc,
            marker_color=[category_colors.get(x, "#CCCCCC") for x in loadings.index]  # fallback to gray
        ))
    fig.update_layout(
        title="PCA Component Loadings",
        yaxis_title="Loading Value",
        barmode="group",
        template="plotly_white"
    )
    return fig
