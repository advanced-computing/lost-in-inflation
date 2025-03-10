# content.py

USED_DATASETS = """
- Daily Inflation projection data from the Fed: [Cleveland Fed Inflation Nowcasting](https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting)
- (Potentially) Daily gas averages by state: [AAA State Gas Price Averages](https://gasprices.aaa.com/state-gas-price-averages/) as well as other alternative data showcasing the impact of inflation on consumers.
- Inflation data from other countries - TBD based on the below considerations.
"""  

RESEARCH_QUESTIONS = """
Expecting increased use of tariffs by the new Trump administration, we will try to answer the following:
- Can we see in real time the effects of Trump's tariffs on inflation in the United States?
- Are American consumers experiencing more inflation compared to their [Canadian*] and [Mexican*] counterparts? (*subject to change based on trajectory of trade policy)
"""

GC_LINK = """
[Google Colab Notebook](https://colab.research.google.com/drive/1BpQXcvX4XtfhNl1k0CyKkKmxlMFvOyDh?usp=sharing)
"""

TARGET_VIS = """
Time series analysis of inflation (potentially overlaid by tariff imposition dates & other alternative measures of inflation)
"""

KNOWN_UNKNOWN = """
- We don’t know when exactly the tariffs will be implemented (if at all), as this is an active discussion with frequent updates.
- There are many factors affecting inflation, and we won’t know all the reasons when trying to draw conclusions from the data.
"""

CHALLENGES = """
- Technical difficulty in accessing gas prices data through API.
- Unifying measures of inflation (baskets of goods used to measure inflation could be different between countries).
- Different levels of data availability and publishing frequency between sources.
"""

INSIGHTS = """
- One major insight is that establishing the relation requires more than 1-2 datasets and requires regression analysis, not only analyzing charts.
- Another insight is that the implementation of announced tariffs wasn't as expected; it was delayed twice, which reduces chances of witnessing the relation of interest.
"""

ADJUSTMENTS= """
- We will narrow the scope in two ways:
  - We will focus on PCE metrics to avoid confusion with CPI metrics.
  - We initially had a large scope geographically, so we will narrow the scope to the US to have more targeted insights.
- We will highlight major policy updates (e.g., tariff announcements and implementation).
"""  


INTRO_TEXT = """
The following chart shows 2 main measures of inflation as projected Month-over-Month percent changes:

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

