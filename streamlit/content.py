# content.py

INTRO_TEXT = """
The following chart shows 4 main measures of inflation as projected Month-over-Month percent changes:

- **CPI** measures consumer price changes for a fixed basket of goods and services.
- **Core CPI** excludes food and energy for a clearer inflation trend.
- **PCE** tracks consumer spending, adjusting for changes in behavior and a broader range of goods.
- **Core PCE** excludes food and energy, serving as the Fed’s preferred inflation gauge.

The Cleveland Fed produces nowcasts (a combination of the word now and forecasts) of the current period's rate of inflation before the official CPI or PCE inflation data are released. 
Such forecasts try to give a sense of where inflation is now and where it is likely to be in the future by relying on high-frequency data, such as daily oil and gas prices.
We are using such nowcasts to get a sense of daily expectations around PCE monthly changes in order to assess co-movement with other data sets, such as the price index for Chinese imports into the U.S.
While the below chart gauges historical co-movement on a monthly basis, the nowcast above will allow us to view expectations for the month ahead before official CPI & PCE data are released.
This data is thus key for testing our hypothesis of increased inflation as a result of more tariffs.

**Our data set:** [Cleveland Fed Nowcasting](https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting)
"""

PCE_CHINA_TEXT = """
The second chart links inflation, represented by **PCE**, with the price of imports from **China** during the first tariff war. 
The metric used is the **Import Export Price Index (MXP)**, which measures the price changes of goods and services traded with the mentioned country.

While it's not possible to correctly assess correlation without running regression analysis, the chart shows some level of co-movement, particularly from mid-2021 to 2025.
Our interest is in analyzing phases of the trade wars with China and their correlation to the **PCE inflation marker**.
In the next phase of our analysis, we will begin looking into such co-movements by doing **regression analyses** of this data and overlaying our current charts with **tariff implementation dates** and other pertinent data sets that we intend to add.

**Data Sources:**  
- [MXP Data](https://data.bls.gov/pdq/SurveyOutputServlet)  
- [Historical PCE](https://apps.bea.gov/iTable/)
"""
