import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import time
import altair as alt
import plotly.graph_objects as go

# Team Description
st.title("Lost-in-Inflation Team")
st.subheader("Team Members: Isaura Arias and Ibrahim Alangari")

# Loading message
st.write("Loading inflation data")

# Progress bar
latest_iteration = st.empty()
bar = st.progress(0)

# Simulating loading process
for i in range(100):
    latest_iteration.text(f'Loading {i+1}')
    bar.progress(i + 1)
    time.sleep(0.05)

st.write("...Let's see what we got")

# Fed inflation data
df = pd.read_csv("streamlit/monthly-inflation-data.csv")
df['Label'] = pd.to_datetime(df['Label'])
df = df.set_index('Label')

# Plotly code for graph 
fig_inflation = go.Figure()

for inflation_type in df.columns:
    fig_inflation.add_trace(go.Scatter(
        x=df.index,
        y=df[inflation_type],
        mode='lines',
        name=inflation_type
    ))

fig_inflation.update_layout(
    title="Monthly Inflation Nowcasting by the Federal Reserve",
    xaxis_title="Date - 2025",
    yaxis_title="Inflation Rate %",
    legend_title="Inflation Type",
    width=1200,
    height=600
)

# Fed inflation Chart
st.plotly_chart(fig_inflation, use_container_width=True)

st.write(""" 
         The Cleveland Fed produces nowcasts (a combination of the word now and forecasts) of the current period's rate of inflation in a given month or quarter—before the official CPI or PCE inflation data are released. 
         Such forecasts try to give a sense of where inflation is now and where it is likely to be in the future by relying on high frequency data, such as daily oil and gas prices.
         We are using such nowcasts to get a sense of daily expectations around PCE monthly changes in order to assess comovement with other data sets, such as the price index for Chinese imports into the U.S.
         While the below chart gauges historical co-movement on a monthly basis, the nowcase above will allow us to view expectations for the month ahead before official CPI & PCE data are released.
         This data is thus key for testing our hypothesis of increased inflation as a result of more tariffs.
         Our data set: https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting 
         """)

# Code for the second chart's data
china_mxp_path = r'C:\repos\lost-in-inflation\streamlit\EIUCOCHNTOT.csv'
pce_path = r'C:\repos\lost-in-inflation\streamlit\MoM PCE.csv'

china_mxp = pd.read_csv(china_mxp_path)
pce = pd.read_csv(pce_path)

# making sure both datasets are in datetime format
pce['Date'] = pd.to_datetime(pce['Year'].astype(str) + '-' + pce['Month'], format='%Y-%b')
china_mxp['Date'] = pd.to_datetime(china_mxp['Year'].astype(str) + '-' + china_mxp['Period'].str[1:], format='%Y-%m')

# Cleaning the data by dropping year/month columns & filtering desired timeframe
pce = pce.drop(columns=['Year', 'Month'])
china_mxp = china_mxp.drop(columns=['Year', 'Period'])
china_mxp_18_24 = china_mxp[(china_mxp['Date'] >= '2018-01-01') & (china_mxp['Date'] <= '2024-12-12')]

# Creating a Plotly figure
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=pce['Date'],
    y=pce['PCE'],
    name='PCE',
    yaxis='y1',
    mode='lines'
))
fig.add_trace(go.Scatter(
    x=china_mxp_18_24['Date'],
    y=china_mxp_18_24['ChinaMXP'],
    name='China MXP',
    yaxis='y2',
    mode='lines'
))

# Detailing graph layout
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

st.plotly_chart(fig, use_container_width=True)

st.write("""
         While it's not possible to correctly assess correlation without running regression analysis, the chart shows some level of co-movement, particularly from mid-2021 to 2025.
         In the next phase of our analysis, we will begin looking into such co-movemennts by doing regression analyses of this data and other pertinent data sets that we intend to add.
         """)
