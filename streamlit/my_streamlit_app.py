import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import altair as alt

# Team Description
st.title("Lost-in-Inflation Team")
st.subheader("Team Members: Isaura Arias and Ibrahim Alangari")

# Display a loading message
st.write("Loading inflation data")

# Add a placeholder for progress bar
latest_iteration = st.empty()
bar = st.progress(0)

# Simulating loading process
for i in range(100):
    latest_iteration.text(f'Loading {i+1}')
    bar.progress(i + 1)
    time.sleep(0.01)

st.write("...Let's see what we got")

# Load and Process Data
df = pd.read_csv("streamlit/inflationdata2025.csv")
df['Label'] = pd.to_datetime(df['Label'])
df = df.set_index('Label')

# Convert Data for Altair (Long Format)
df_long = df.reset_index().melt("Label", var_name="Inflation Type", value_name="Rate")

# Create Interactive Chart
chart = (
    alt.Chart(df_long)
    .mark_line()
    .encode(
        x=alt.X("Label:T", title="Date - 2025"),  # Temporal x-axis
        y=alt.Y("Rate:Q", title="Inflation Rate"),
        color="Inflation Type:N",
        tooltip=["Label:T", "Inflation Type:N", "Rate:Q"],  # Hover tooltips
    )
    .interactive()  # Enable zooming & panning
    .properties(title="Inflation Nowcasting by the Federal Reserve", width=1200, height=600)
)

# Display in Streamlit
st.altair_chart(chart, use_container_width=True)