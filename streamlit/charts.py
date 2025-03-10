import plotly.graph_objects as go

def create_inflation_chart(df):
    """Creates a Plotly chart for PCE and Core PCE inflation data - leaving out all CPI data, which are partially missing."""
    fig = go.Figure()

    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))

    fig.update_layout(
        title="Monthly PCE & Core PCE Inflation - Federal Reserve",
        xaxis_title="Date",
        yaxis_title="Inflation Rate %",
        legend_title="Inflation Type",
        width=1200,
        height=600
    )
    return fig


def create_pce_china_mxp_chart(pce, china_mxp):
    if 'PCE' not in pce.columns or 'ChinaMXP' not in china_mxp.columns:
        raise ValueError("Missing required columns in data.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pce['Date'], y=pce['PCE'], name='PCE', yaxis='y1', mode='lines'))
    fig.add_trace(go.Scatter(x=china_mxp['Date'], y=china_mxp['ChinaMXP'], name='China MXP', yaxis='y2', mode='lines'))

    fig.update_layout(
        title="PCE Inflation vs. China MXP",
        xaxis_title="Date",
        yaxis=dict(title="PCE Inflation Rate %"),
        yaxis2=dict(title="China MXP Index", overlaying="y", side="right"),
        width=1200,
        height=600
    )
    return fig
