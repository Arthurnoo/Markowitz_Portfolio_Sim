import os
import pickle
import sys
import subprocess
import yfinance as yf
import pandas as pd

# 📌 Vérifier et installer `yfinance` si nécessaire
package = "yfinance"
try:
    import yfinance
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 📌 Chemin vers le fichier des tickers validés
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Récupère le chemin absolu du script en cours
DATA_DIR = os.path.join(BASE_DIR, "../data")  # Remonte dans `data`
FILE_PATH = os.path.join(DATA_DIR, "validated_tickers.pkl")  # Chemin final du fichier

def get_validated_tickers():
    """
    Charge les tickers validés depuis le fichier `validated_tickers.pkl`.
    
    Returns:
        list: Liste des tickers validés.
    """
    try:
        if not os.path.exists(FILE_PATH):
            print(f"❌ Fichier introuvable : '{FILE_PATH}'\nAssurez-vous que le fichier a été créé via `questions.py`.")
            return None
        with open(FILE_PATH, "rb") as f:
            tickers = pickle.load(f)
        if not tickers:
            print("⚠️ Aucun ticker enregistré. Veuillez valider des tickers via l'interface Streamlit.")
            return None
        return tickers
    except Exception as e:
        print(f"❌ Erreur lors du chargement des tickers : {e}")
        return None

# 📌 Vérification que le fichier existe bien
tickers_selected = get_validated_tickers()

if tickers_selected:
    print("\n✅ Tickers validés par l'utilisateur :")
    print(tickers_selected)
else:
    print("❌ Aucun ticker validé.")

def download_data(tickers, period="5y", interval="1d"):
    """
    Télécharge les données financières des tickers sélectionnés.
    
    Args:
        tickers (list): Liste des tickers.
        period (str): Période d'historique ("1y", "5y", "max").
        interval (str): Intervalle des données ("1d", "1wk").
    
    Returns:
        pd.DataFrame: Prix ajustés des tickers.
    """
    try:
        data = yf.download(tickers, period=period, interval=interval, group_by="ticker")

        # 📌 Vérifier si 'Adj Close' est dans le DataFrame multi-indexé
        if isinstance(data.columns, pd.MultiIndex):
            try:
                adj_close = data.xs("Adj Close", level=1, axis=1)
                print("✅ 'Adj Close' extrait depuis MultiIndex.")
            except KeyError:
                print("⚠️ 'Adj Close' absent du MultiIndex. Vérification de 'Close'.")
                adj_close = data.xs("Close", level=1, axis=1)
        elif "Adj Close" in data:
            adj_close = data["Adj Close"]
            print("✅ 'Adj Close' trouvé !")
        elif "Close" in data:
            adj_close = data["Close"]
            print("⚠️ 'Adj Close' introuvable. Utilisation de 'Close'.")
        else:
            print("❌ Aucune donnée 'Adj Close' ou 'Close' disponible.")
            return None

        return adj_close.dropna()  # Supprime les lignes avec NaN

    except Exception as e:
        print(f"❌ Erreur lors du téléchargement des données : {e}")
        return None

def calculate_returns(data):
    """
    Calcule les rendements journaliers des actifs.

    Args:
        data (pd.DataFrame): Données des prix ajustés.

    Returns:
        pd.DataFrame: Rendements journaliers.
    """
    return data.pct_change().dropna()

def calculate_statistics(returns):
    """
    Calcule les rendements moyens, la volatilité et la matrice de covariance en utilisant Adj Close uniquement.

    Args:
        returns (pd.DataFrame): Rendements journaliers.

    Returns:
        dict: Contient les rendements moyens, volatilité et covariance.
    """
    mean_returns = returns.mean()  # 📌 Rendement moyen journalier
    annualized_returns = mean_returns * 252  # 📌 Conversion en rendement annuel
    
    volatility = returns.std()  # 📌 Volatilité journalière
    annualized_volatility = volatility * (252 ** 0.5)  # 📌 Conversion en volatilité annuelle

    cov_matrix = returns.cov()  # 📌 Matrice de covariance des rendements journaliers

    return {
        "mean_returns": mean_returns,
        "annualized_returns": annualized_returns,
        "volatility": volatility,
        "annualized_volatility": annualized_volatility,
        "covariance_matrix": cov_matrix
    }

def analyze_portfolio():
    """
    Récupère les tickers validés, télécharge les données et calcule les statistiques.
    """
    tickers = get_validated_tickers()
    if not tickers:
        return

    print(f"📌 Tickers sélectionnés : {tickers}")

    # 📌 Télécharger les prix ajustés des tickers
    data = download_data(tickers)
    if data is None or data.empty:
        print("❌ Échec de la récupération des données.")
        return

    # 📌 Calcul des rendements et statistiques
    returns = calculate_returns(data)
    stats = calculate_statistics(returns)

    # 📌 Affichage des résultats
    print("\n📈 **Rendements Moyens Journaliers**")
    print(stats["mean_returns"])

    print("\n📈 **Rendements Moyens Annuels**")
    print(stats["annualized_returns"])

    print("\n📊 **Volatilité Journalière**")
    print(stats["volatility"])

    print("\n📊 **Volatilité Annuelle**")
    print(stats["annualized_volatility"])

    print("\n🔄 **Matrice de Covariance**")
    print(stats["covariance_matrix"])

    # 📌 Matrice de corrélation
    corr_matrix = returns.corr()

    print("\n🔄 **Matrice de Corrélation**")
    print(corr_matrix)


    return stats  # Renvoie les statistiques pour d'autres utilisations

# 📌 Exécuter l'analyse si ce script est lancé directement
if __name__ == "__main__":
    analyze_portfolio()