import plotly.graph_objects as go
from datetime import datetime

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
    if 'PCE' not in pce.columns or 'ChinaMXP' not in china_mxp.columns:
        raise ValueError("Missing required columns in data.")

    fig = go.Figure()

    # Add main data lines
    fig.add_trace(go.Scatter(x=pce['Date'], y=pce['PCE'], name='PCE', yaxis='y1', mode='lines'))
    fig.add_trace(go.Scatter(x=china_mxp['Date'], y=china_mxp['ChinaMXP'], name='China MXP', yaxis='y2', mode='lines'))

    # Tariff event markers
    tariff_events = [
        {"date": datetime(2018, 3, 22), "label": "Tariff Announced"},
        {"date": datetime(2018, 7, 6), "label": "Round 1 Tariffs"},
        {"date": datetime(2018, 9, 24), "label": "Round 3 Tariffs"},
        {"date": datetime(2019, 5, 10), "label": "$200B Raised to 25%"},
        {"date": datetime(2020, 1, 15), "label": "Phase One Deal"},
        {"date": datetime(2021, 6, 9), "label": "Biden Keeps China Tariffs"},
    ]

    # Add vertical lines + manual annotations
    for event in tariff_events:
        event_date = event["date"]
        label_text = f"{event['label']} ({event_date.strftime('%Y-%m-%d')})"

        # Add vertical line using shape
        fig.add_shape(
            type="line",
            x0=event_date, x1=event_date,
            y0=0, y1=1,
            xref="x", yref="paper",
            line=dict(color="red", width=1, dash="dash")
        )

        # Add annotation near top
        fig.add_annotation(
            x=event_date,
            y=1,
            xref="x",
            yref="paper",
            text=label_text,
            showarrow=False,
            font=dict(color="red", size=10),
            align="left",
            xanchor="left",
            yanchor="bottom"
        )

    # Layout
    fig.update_layout(
        title="PCE Inflation vs. China MXP",
        xaxis_title="Date",
        yaxis=dict(title="PCE Inflation Rate %"),
        yaxis2=dict(title="China MXP Index", overlaying="y", side="right"),
        width=1200,
        height=600
    )

    return fig