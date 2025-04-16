from datetime import datetime
import pandas as pd
import os
import time
from glob import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

def download_current_month_csv(save_dir="streamlit/fed_data_per_month"):
    now = datetime.now()
    year_month_str = f"{now.year}-{now.month}"
    filename = f"{year_month_str}.csv"
    save_path = os.path.join(save_dir, filename)

    HEADLESS = False  # 👈 Toggle this as needed
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.path.abspath(save_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("🌐 Launching browser to fetch Cleveland Fed table...")
        driver.get("https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting")

        # Accept cookie banner if visible
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            ).click()
            print("🍪 Accepted cookies.")
        except TimeoutException:
            print("🍪 No cookie popup found.")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        print("✅ Page headline loaded.")

        # Scroll and expand Monthly section
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.95);")
        print("📜 Scrolled to bottom to reveal monthly section.")
        time.sleep(2)

        accordion_xpath = '//*[@id="section-title-2-19"]/h5/button/div/div/div'
        accordion_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, accordion_xpath))
        )
        driver.execute_script("arguments[0].click();", accordion_button)
        print("📂 Clicked Monthly (month-over-month) accordion")

        time.sleep(2)

        # Try Option 1 – direct XPath click
        try:
            csv_button_xpath = '/html/body/div[2]/main/div/div[3]/div[1]/div[5]/div/ul/li[1]/div[2]/div/div[1]/div/chart-nowcasting/button[2]'
            csv_button = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, csv_button_xpath))
            )
            csv_button.click()
            print("⬇️ Clicked Download CSV button via direct XPath.")
        except TimeoutException:
            print("⚠️ Direct XPath click failed, trying hover method...")

            try:
                # Hover over visible inner chart element
                chart_inner_xpath = '//chart-nowcasting//*[name()="svg" or name()="canvas" or name()="div"]'
                chart_target = WebDriverWait(driver, 8).until(
                    EC.visibility_of_element_located((By.XPATH, chart_inner_xpath))
                )
                ActionChains(driver).move_to_element(chart_target).perform()
                print("🖱 Hovered over chart's visible inner element to trigger buttons.")
                time.sleep(1)

                csv_button = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, csv_button_xpath))
                )
                csv_button.click()
                print("⬇️ Clicked Download CSV button after hover.")
            except Exception as hover_fail:
                print(f"⚠️ Hover method failed: {hover_fail}")
                print("⚠️ Trying raw button scan...")

                try:
                    buttons = driver.find_elements(By.XPATH, '//chart-nowcasting//button')
                    print(f"🔍 Found {len(buttons)} buttons inside <chart-nowcasting>:")
                    target_button = None
                    for i, btn in enumerate(buttons):
                        try:
                            text = btn.text.strip()
                            print(f"  • Button {i+1}: displayed={btn.is_displayed()}, text='{text}'")
                            if "Download CSV" in text and btn.is_displayed():
                                target_button = btn
                        except Exception:
                            print(f"  • Button {i+1}: failed to read properties.")

                    if target_button:
                        driver.execute_script("arguments[0].click();", target_button)
                        print("✅ Clicked 'Download CSV' button via JS click().")
                    else:
                        raise Exception("❌ No interactable 'Download CSV' button found.")
                except Exception as scan_fail:
                    driver.save_screenshot("csv_button_error.png")
                    with open("debug_source.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    print("❌ All methods failed. Screenshot and page source saved.")
                    raise scan_fail

        # Wait for file to download
        # Wait for download to complete
        timeout = 15  # seconds
        start_time = time.time()
        downloaded_file = None

        print("⏳ Waiting for CSV download to finish...")

        while time.time() - start_time < timeout:
            files = [
                f for f in os.listdir(save_dir)
                if f.endswith(".csv") and "Month-Over-MonthPercentChange" in f
            ]
            if files:
                # Assume most recent file is the downloaded one
                downloaded_file = max(
                    [os.path.join(save_dir, f) for f in files],
                    key=os.path.getctime
                )
                if not downloaded_file.endswith(".crdownload"):
                    break
            time.sleep(1)

        if not downloaded_file or downloaded_file.endswith(".crdownload"):
            raise FileNotFoundError("❌ Downloaded CSV file not found or still incomplete.")

        # Safely remove existing monthly file
        if os.path.exists(save_path):
            os.remove(save_path)

        # Rename with standard format
        os.rename(downloaded_file, save_path)
        print(f"✅ Saved monthly CSV as: {save_path}")

        return save_path

    except Exception as e:
        driver.save_screenshot("debug_screen.png")
        print("🖼 Screenshot saved: debug_screen.png")
        raise e

    finally:
        driver.quit()


def combine_clean_monthly_csvs(
    input_dir="streamlit/fed_data_per_month",
    output_file="streamlit/fed_data_per_month/clean_monthly.csv"
):
    all_files = sorted(glob(os.path.join(input_dir, "2025-*.csv")))
    dfs = []

    for file in all_files:
        df = pd.read_csv(file)

        # Normalize column names just for checking
        df.columns = df.columns.str.strip()

        required_cols = {"Label", "PCE Inflation", "Core PCE Inflation"}
        if not required_cols.issubset(set(df.columns)):
            print(f"⚠️ Skipping {file} — missing expected columns: {df.columns.tolist()}")
            continue

        # Drop if key columns are missing values
        df = df.dropna(subset=["PCE Inflation", "Core PCE Inflation"])

        # Extract full date from MM/DD using filename for year/month
        year, month = os.path.basename(file).replace(".csv", "").split("-")
        df["Label"] = pd.to_datetime(
            df["Label"].apply(lambda x: f"{year}/{month}/{str(x).split('/')[-1]}"),
            format="%Y/%m/%d",
            errors="coerce"
        )

        # Drop rows where date parsing failed
        df = df.dropna(subset=["Label"])

        dfs.append(df)

    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        combined.sort_values("Label", inplace=True)
        combined.to_csv(output_file, index=False)
        print(f"✅ Combined CSV saved: {output_file}")
    else:
        print("❌ No valid monthly data to combine.")
