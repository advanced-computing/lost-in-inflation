import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

def create_inflation_chart(df):
    """Creates a Plotly chart for PCE and Core PCE inflation data with 2025 tariff events."""
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

    # Tariff event dates (announced + implemented only)
    tariff_events = [
        {"date": datetime(2025, 2, 1), "label": "Tariffs Announced\nCanada, Mexico, China"},
        {"date": datetime(2025, 3, 4), "label": "Tariffs Implemented\nCanada, Mexico, China"},
    ]

    # Add vertical lines and text annotations manually
    for event in tariff_events:
        # Add red dashed vertical line
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
        # Add annotation
        fig.add_annotation(
            x=event["date"],
            y=1,
            xref="x",
            yref="paper",
            text=event["label"] + f"<br>({event['date'].strftime('%Y-%m-%d')})",
            showarrow=False,
            font=dict(color="red"),
            align="left"
        )

    # Layout settings
    fig.update_layout(
        title="Inflation Rate with 2025 Tariff Events",
        xaxis_title="Date",
        yaxis_title="Inflation Rate (%)",
        legend_title="Inflation Metrics",
        width=1200,
        height=600
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
