import subprocess
import sys

# Check if lxml is installed, if not install it
try:
    import lxml
except ImportError:
    print("lxml is not installed. Installation in progress...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "lxml"])


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from io import StringIO  # To create a file object in memory


def get_SnP_tickers():
    """
    Retrieves a list of ticker symbols for all companies in the S&P 500 index.
    """
    # URL of the page
    url = 'https://www.slickcharts.com/sp500'

    # Request with a User-Agent
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code != 200:
        raise Exception(f"Échec de la requête : {response.status_code}")

    # HTML analysis with BeautifulSoup
    soup = bs(response.text, "lxml")
    stats = soup.find('table', class_='table table-hover table-borderless table-sm')

    # Using StringIO to avoid FutureWarning
    table_html = str(stats)
    table_buffer = StringIO(table_html)
    df = pd.read_html(table_buffer)[0]

    # Cleaning columns
    tickers = df['Symbol'].dropna().tolist()
    return tickers


# Call the function
tickers = get_SnP_tickers()
print("S&P 500 tickers :", tickers)