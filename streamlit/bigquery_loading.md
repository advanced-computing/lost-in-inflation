Lab 10

Upon observation, we are currently only loading our monthly-inflation-data.csv via BigQuery.
The process is as follows: Using the Python BigQuery client, our local csv is loaded into BigQuery. From here, the data is queried directly into Streamlit. This process takes approximately 3 seconds to load locally and appears to load in 1-2 seconds on our website: https://lost-in-inflationgit-project.streamlit.app/.

I then changed the code to load our MoM PCE.csv & EIUCOCJNTOT.csv via BigQuery as well and incorporated code to track loading time akin to the following: {end_time - start_time:.2f}. Although our csv names are not great, the latter two are used for our "China MXP chart" (our second chart).

Upon running the app now, it prints how long it takes to load each chart. Currently, our first chart on Fed PCE inflation takes 2.67 seconds to load and our second chart is a surprising -0.01 seconds, however possible. 

Our data loadint method:

Within Gbqload.py, we have the line: write_disposition="WRITE_APPEND",

This instructs BigQuery to add new data to the table without deleting or replacing data that is already there. Although our team is not concerned of data changing, as our Fed inflation data gets updated almost daily into new rows (thus never altering what is already there), this is the best method for this project. We seek to keep a time-series of inflation data, and in chart 1, inflation expectations specifically, so we need data to reflect sentiment as it was at that period in time. Replacements are therefore not acceptable. We will continue to employ this method for all our data sets, to ensure data integrity, as we will be adding several others soon for statistical analysis. 