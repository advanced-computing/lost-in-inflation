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


#refactored code to read data from folder - also added start_date parameter to filter data
def load_csv_data(filepath, index_col=None, date_col=None, drop_cols=None, create_date_from=None, period_col=None, start_date=None):
    df = pd.read_csv(filepath)

    # If date needs to be created from multiple columns (e.g., Year & Month)
    if create_date_from:
        df['Date'] = pd.to_datetime(df[create_date_from[0]].astype(str) + '-' + df[create_date_from[1]], format='%Y-%b')

    # Handle Period column if it's in "M01" format (China MXP)
    elif period_col:
        df['Month'] = df[period_col].str[1:].astype(int)  # Remove "M" and convert to int
        df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%m')

    # Convert a single column into datetime
    elif date_col:
        df[date_col] = pd.to_datetime(df[date_col])

    # Drop unnecessary columns
    if drop_cols:
        df = df.drop(columns=drop_cols)
    
    # Filter data if start_date is provided
    if start_date:
        df = df[df['Date'] >= start_date]

    # Set index if required
    if index_col:
        df = df.set_index(index_col)

    return df

# Reading Fed inflation data
df = load_csv_data("streamlit/monthly-inflation-data.csv", index_col="Label", date_col="Label")
# Code for the second chart's data - modified to be readble in Streamlit Cloud
china_mxp = load_csv_data(
    "./streamlit/EIUCOCHNTOT.csv",
    period_col="Period",  
    drop_cols=['Year', 'Period'],
    start_date="2018-01-01"  # Filter from 2018 onwards
)
pce = load_csv_data(
    "./streamlit/MoM PCE.csv",
    drop_cols=['Year', 'Month'],  # Drop after creating Date
    create_date_from=['Year', 'Month']  # Create 'Date' column
)

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
    title="Monthly Percent Change of Inflation - Nowcasting by the Federal Reserve",
    xaxis_title="Date - 2025",
    yaxis_title="Inflation Rate %",
    legend_title="Inflation Type",
    width=1200,
    height=600
)

st.write("""The following chart shows 4 main measures of inflation as projected Month-over-Month percent changes:
CPI measures consumer price changes for a fixed basket of goods and services.
Core CPI excludes food and energy for a clearer inflation trend.
PCE tracks consumer spending, adjusting for changes in behavior and a broader range of goods.
Core PCE excludes food and energy, serving as the Fed’s preferred inflation gauge.""")

# Fed inflation Chart
st.plotly_chart(fig_inflation, use_container_width=True)

st.write(""" 
         The Cleveland Fed produces nowcasts (a combination of the word now and forecasts) of the current period's rate of inflation before the official CPI or PCE inflation data are released. 
         Such forecasts try to give a sense of where inflation is now and where it is likely to be in the future by relying on high frequency data, such as daily oil and gas prices.
         We are using such nowcasts to get a sense of daily expectations around PCE monthly changes in order to assess comovement with other data sets, such as the price index for Chinese imports into the U.S.
         While the below chart gauges historical co-movement on a monthly basis, the nowcase above will allow us to view expectations for the month ahead before official CPI & PCE data are released.
         This data is thus key for testing our hypothesis of increased inflation as a result of more tariffs.
         Our data set: https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting 
         """)


st.write("""The second chart links inflation, represented by PCE, with price of imports from China during the first tariff war. 
         The metric used is the Import Export Price Index (MXP), which measures the price changes of goods and services traded with the mentioned country """)



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
    x=china_mxp['Date'],
    y=china_mxp['ChinaMXP'],
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
         Our interest is on analysing phases of the trade wars with China and their correlation to the PCE inflation marker.
         In the next phase of our analysis, we will begin looking into such co-movemennts by doing regression analyses of this data and overlaying our current charts with tariff implementation dates and other pertinent data sets that we intend to add.
         MXP Source: https://data.bls.gov/pdq/SurveyOutputServlet
         Historical PCE: https://apps.bea.gov/iTable/?reqid=19&step=3&isuri=1&1921=survey&1903=84&_gl=1*htjsf2*_ga*ODM2NzMyNzk3LjE3Mzk5MjI0NjQ.*_ga_J4698JNNFT*MTc0MDAxNjgxMS4yLjAuMTc0MDAxNjgxMS42MC4wLjA.#eyJhcHBpZCI6MTksInN0ZXBzIjpbMSwyLDMsM10sImRhdGEiOltbIk5JUEFfVGFibGVfTGlzdCIsIjg0Il0sWyJDYXRlZ29yaWVzIiwiU3VydmV5Il0sWyJGaXJzdF9ZZWFyIiwiMjAxOCJdLFsiTGFzdF9ZZWFyIiwiMjAyNCJdLFsiU2NhbGUiLCIwIl0sWyJTZXJpZXMiLCJNIl1dfQ==
         """)
