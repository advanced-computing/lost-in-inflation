#Project Title: Daily U.S. Inflation Forecast to Trump's Trade War

Major updates as of 4/16/2025 (IA to refine):
Selenium scraping
CSV version control
Incremental BigQuery loading

Tools folder added: Chromedriver added to use Selnium. The app will use Selenium and ChromeDriver to download data from the Cleveland Fed. The chromedriver.exe file is bundled under /tools. If you're using a different OS or Chrome version, download a compatible version from here and replace the file.


Project Description: Our team will focus on tracking daily U.S. inflation data projections by the Federal Reserve and interlay the constantly changing trade policy enviroment under President Trump. Economists, market participants, and consumers alike are expecting an inflationary environment in the short term. Our analysis seeks to test this main hypothesis. 

Status: Currently, our team is at the phase of integrating various statistical methods with our time series of inflation expectations chart.For the purpose of our project, we also have a secodn chart tracking the correlation of historical PCE inflation and a price import index for goods incoming from China. Because our statistical analysis is in the works, the charts are quite basic and this portion of the app will change significantly in the coming days & weeks.

To be updated - do not follow currently...
To get this app working, please follow the following instructions:
(1) Clone our repository locally using: https://github.com/advanced-computing/lost-in-inflation.git
(2) Create a virtual environment using the command python -m venv .venv
(3) Activate virtual environment using the code that works for your platform, such as venv\Scripts\activate for Windows
(4) Install requirements.txt to ensure you have all the packages needed. If you encounter errors, such as "no module named plotly found", install it manually using "pip install plotly" to bypass this type of error. No further errors have yet been identified. For all other errors, you might need to rely on external sources to troubleshoot  
(5) Build the app locally by the opening the python file "my_streamlit_app.py" and running it using ctrl d
(6) Next, open the app locally using the command in your bash terminal: streamlit run streamlit/my_streamlit_app.py

Our deployed app can be accessed publicly via: https://lost-in-inflationgit-project.streamlit.app/




