import requests
from bs4 import BeautifulSoup

# Define the URL and headers
url = "https://www.lithuania.travel/en/category/what-is-lithuania"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

# Fetch and parse the page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find all paragraph tags and filter out empty ones
paragraphs = [p.text.strip() for p in soup.find_all("p") if p.text.strip()]

# Print all paragraphs to check content
for i, p in enumerate(paragraphs[:5]):  # Print first 5 non-empty paragraphs
    print(f"Paragraph {i+1}: {p}\n")
