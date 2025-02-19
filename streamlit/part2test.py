import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set the title for the Streamlit app
st.title("PCE and China MXP Over Time")

# Define file paths using raw string literals to avoid escape sequence issues
china_mxp_path = r'C:\repos\lost-in-inflation\streamlit\EIUCOCHNTOT.csv'
pce_path = r'C:\repos\lost-in-inflation\streamlit\MoM PCE.csv'

# Read CSV files from the local folder
china_mxp = pd.read_csv(china_mxp_path)
pce = pd.read_csv(pce_path)

# Convert 'Year' and 'Month' in pce to a datetime column
pce['Date'] = pd.to_datetime(pce['Year'].astype(str) + '-' + pce['Month'], format='%Y-%b')

# Convert 'Year' and 'Period' in china_mxp to a datetime column
china_mxp['Date'] = pd.to_datetime(china_mxp['Year'].astype(str) + '-' + china_mxp['Period'].str[1:], format='%Y-%m')

# Dropping year/month columns as they're no longer needed
pce = pce.drop(columns=['Year', 'Month'])
china_mxp = china_mxp.drop(columns=['Year', 'Period'])

# Create a subset of China MXP data from 2018 to 2024
china_mxp_18_24 = china_mxp[(china_mxp['Date'] >= '2018-01-01') & (china_mxp['Date'] <= '2024-12-12')]

# Create a Plotly figure with two y axes
fig = go.Figure()

# Add first line for PCE
fig.add_trace(go.Scatter(
    x=pce['Date'],
    y=pce['PCE'],
    name='PCE',
    yaxis='y1',
    mode='lines'
))

# Add second line for China MXP
fig.add_trace(go.Scatter(
    x=china_mxp_18_24['Date'],
    y=china_mxp_18_24['ChinaMXP'],
    name='China MXP',
    yaxis='y2',
    mode='lines'
))

# Update the layout of the chart using the new title configuration
fig.update_layout(
    title="PCE and China MXP Over Time",
    xaxis=dict(title="Date"),
    yaxis=dict(
        title=dict(text="PCE", font=dict(color="blue")),
        tickfont=dict(color="blue"),
        side="left"
    ),
    yaxis2=dict(
        title=dict(text="China MXP", font=dict(color="red")),
        tickfont=dict(color="red"),
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0.1, y=1),
)

# Display the figure in the Streamlit app
st.plotly_chart(fig, use_container_width=True)

# Add a conclusion text below the graph
st.write("While it's not possible to correctly assess correlation without running regression analysis, the chart shows some level of co-movement, particularly from mid-2021 to 2025.")
