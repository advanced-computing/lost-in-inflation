import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import time
import altair as alt
import plotly.graph_objects as go

# Team Description
st.title("Lost-in-Inflation Team")
st.subheader("Team Members: Isaura Arias and Ibrahim Alangari")

# Loading bar is turned into a neater function 
def show_loading_bar():
    """Simulates a loading bar in Streamlit."""
    st.write("Loading inflation data")
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        latest_iteration.text(f'Loading {i+1}')
        bar.progress(i + 1)
        time.sleep(0.05)

    st.write("...Let's see what we got")

#Calling the loading bar
show_loading_bar()

# Fed inflation data
df = pd.read_csv("streamlit/monthly-inflation-data.csv")
df['Label'] = pd.to_datetime(df['Label'])
df = df.set_index('Label')

# Refactored inflation chart 
def create_inflation_chart(df):
    """Creates and returns a Plotly figure for Fed MoM inflation data."""
    fig = go.Figure()

    for inflation_type in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[inflation_type],
            mode='lines',
            name=inflation_type
        ))

    fig.update_layout(
        title="Monthly Percent Change of Inflation - Nowcasting by the Federal Reserve",
        xaxis_title="Date - 2025",
        yaxis_title="Inflation Rate %",
        legend_title="Inflation Type",
        width=1200,
        height=600
    )

    return fig

st.write("""The following chart shows 4 main measures of inflation as projected Month-over-Month percent changes:
CPI measures consumer price changes for a fixed basket of goods and services.
Core CPI excludes food and energy for a clearer inflation trend.
PCE tracks consumer spending, adjusting for changes in behavior and a broader range of goods.
Core PCE excludes food and energy, serving as the Fed’s preferred inflation gauge.""")

# Calling the Fed inflation function
st.plotly_chart(create_inflation_chart(df), use_container_width=True) #updated

st.write(""" 
         The Cleveland Fed produces nowcasts (a combination of the word now and forecasts) of the current period's rate of inflation before the official CPI or PCE inflation data are released. 
         Such forecasts try to give a sense of where inflation is now and where it is likely to be in the future by relying on high frequency data, such as daily oil and gas prices.
         We are using such nowcasts to get a sense of daily expectations around PCE monthly changes in order to assess comovement with other data sets, such as the price index for Chinese imports into the U.S.
         While the below chart gauges historical co-movement on a monthly basis, the nowcase above will allow us to view expectations for the month ahead before official CPI & PCE data are released.
         This data is thus key for testing our hypothesis of increased inflation as a result of more tariffs.
         Our data set: https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting 
         """)

# Code for the second chart's data - modified to be readble in Streamlit Cloud
china_mxp_path = "./streamlit/EIUCOCHNTOT.csv" #this or below can be made DRY
pce_path = "./streamlit/MoM PCE.csv"

china_mxp = pd.read_csv(china_mxp_path)
pce = pd.read_csv(pce_path)

# making sure both datasets are in datetime format
pce['Date'] = pd.to_datetime(pce['Year'].astype(str) + '-' + pce['Month'], format='%Y-%b')
china_mxp['Date'] = pd.to_datetime(china_mxp['Year'].astype(str) + '-' + china_mxp['Period'].str[1:], format='%Y-%m')

# Cleaning the data by dropping year/month columns & filtering desired timeframe
pce = pce.drop(columns=['Year', 'Month'])
china_mxp = china_mxp.drop(columns=['Year', 'Period'])
china_mxp_18_24 = china_mxp[(china_mxp['Date'] >= '2018-01-01') & (china_mxp['Date'] <= '2024-12-12')]


st.write("""The second chart links inflation, represented by PCE, with price of imports from China during the first tariff war. 
         The metric used is the Import Export Price Index (MXP), which measures the price changes of goods and services traded with the mentioned country """)


# Refactoring the second graph
def create_pce_china_mxp_chart(pce, china_mxp):
    """Creates and returns a Plotly figure for PCE and China MXP data."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=pce['Date'],
        y=pce['PCE'],
        name='PCE',
        yaxis='y1',
        mode='lines'
    ))

    fig.add_trace(go.Scatter(
        x=china_mxp_18_24['Date'], # has to reference mxp_18_24 specfically now
        y=china_mxp_18_24['ChinaMXP'],
        name='China MXP',
        yaxis='y2',
        mode='lines'
    ))

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

    return fig

#Calling the second graph function 
st.plotly_chart(create_pce_china_mxp_chart(pce, china_mxp_18_24), use_container_width=True) #updated

st.write("""
         While it's not possible to correctly assess correlation without running regression analysis, the chart shows some level of co-movement, particularly from mid-2021 to 2025.
         Our interest is on analysing phases of the trade wars with China and their correlation to the PCE inflation marker.
         In the next phase of our analysis, we will begin looking into such co-movemennts by doing regression analyses of this data and overlaying our current charts with tariff implementation dates and other pertinent data sets that we intend to add.
         MXP Source: https://data.bls.gov/pdq/SurveyOutputServlet
         Historical PCE: https://apps.bea.gov/iTable/?reqid=19&step=3&isuri=1&1921=survey&1903=84&_gl=1*htjsf2*_ga*ODM2NzMyNzk3LjE3Mzk5MjI0NjQ.*_ga_J4698JNNFT*MTc0MDAxNjgxMS4yLjAuMTc0MDAxNjgxMS42MC4wLjA.#eyJhcHBpZCI6MTksInN0ZXBzIjpbMSwyLDMsM10sImRhdGEiOltbIk5JUEFfVGFibGVfTGlzdCIsIjg0Il0sWyJDYXRlZ29yaWVzIiwiU3VydmV5Il0sWyJGaXJzdF9ZZWFyIiwiMjAxOCJdLFsiTGFzdF9ZZWFyIiwiMjAyNCJdLFsiU2NhbGUiLCIwIl0sWyJTZXJpZXMiLCJNIl1dfQ==
         """)
