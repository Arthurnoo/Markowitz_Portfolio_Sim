import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from io import StringIO  # Pour créer un objet fichier en mémoire


def get_SnP_tickers():
    """
    Retrieves a list of ticker symbols for all companies in the S&P 500 index.
    """
    # URL de la page
    url = 'https://www.slickcharts.com/sp500'

    # Requête avec un User-Agent
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code != 200:
        raise Exception(f"Échec de la requête : {response.status_code}")

    # Analyse du HTML avec BeautifulSoup
    soup = bs(response.text, "lxml")
    stats = soup.find('table', class_='table table-hover table-borderless table-sm')

    # Utilisation de StringIO pour éviter le FutureWarning
    table_html = str(stats)
    table_buffer = StringIO(table_html)
    df = pd.read_html(table_buffer)[0]

    # Nettoyage des colonnes
    tickers = df['Symbol'].dropna().tolist()  # Liste des tickers
    return tickers


# Appeler la fonction
tickers = get_SnP_tickers()
print("Tickers du S&P 500 :", tickers)
print(len(tickers))