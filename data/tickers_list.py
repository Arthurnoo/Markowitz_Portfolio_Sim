import streamlit as st
import pandas as pd

# Titre de la page
st.title("Liste des 50 Principaux Tickers")

# Données des tickers (ajouter les valeurs réelles ici)
data = {
    "Nom de l'Entreprise/Indice": [
        "Apple Inc.", "Microsoft Corp.", "Amazon.com Inc.", "Alphabet Inc. (Class A)",
        "Alphabet Inc. (Class C)", "NVIDIA Corp.", "Tesla Inc.", "Meta Platforms Inc.",
        "Berkshire Hathaway Inc.", "Visa Inc.", "Johnson & Johnson", "Exxon Mobil Corp.",
        "Procter & Gamble Co.", "UnitedHealth Group Inc.", "JPMorgan Chase & Co.",
        "Mastercard Inc.", "Walmart Inc.", "Chevron Corp.", "Home Depot Inc.",
        "Eli Lilly and Co.", "AbbVie Inc.", "PepsiCo Inc.", "Pfizer Inc.", "Coca-Cola Co.",
        "Merck & Co. Inc.", "Intel Corp.", "Cisco Systems Inc.", "Nike Inc.", "Adobe Inc.",
        "Broadcom Inc.", "Costco Wholesale Corp.", "McDonald's Corp.", "Thermo Fisher Scientific Inc.",
        "Texas Instruments Inc.", "Netflix Inc.", "Salesforce Inc.", "QUALCOMM Inc.",
        "Philip Morris International Inc.", "Honeywell International Inc.", "Amgen Inc.",
        "Bristol-Myers Squibb Co.", "Union Pacific Corp.", "General Electric Co.",
        "Danaher Corp.", "NextEra Energy Inc.", "Boeing Co.", "3M Co.", "IBM Corp.",
        "Goldman Sachs Group Inc.", "Citigroup Inc.", "Ford Motor Co."
    ],
    "Ticker": [
        "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "NVDA", "TSLA", "META", "BRK.B", "V",
        "JNJ", "XOM", "PG", "UNH", "JPM", "MA", "WMT", "CVX", "HD", "LLY", "ABBV", "PEP",
        "PFE", "KO", "MRK", "INTC", "CSCO", "NKE", "ADBE", "AVGO", "COST", "MCD", "TMO",
        "TXN", "NFLX", "CRM", "QCOM", "PM", "HON", "AMGN", "BMY", "UNP", "GE", "DHR",
        "NEE", "BA", "MMM", "IBM", "GS", "C", "F"
    ]
}

# Créer un DataFrame
df = pd.DataFrame(data)

# Afficher le tableau
st.table(df)

# Message supplémentaire
st.markdown(
    """
    Vous pouvez copier ces tickers et les utiliser dans le questionnaire principal.
    """
)