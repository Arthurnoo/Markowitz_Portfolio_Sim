import os
import pickle
import subprocess
import sys
import time
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yfinance as yf
import seaborn as sns

# 📌 Définition des chemins des fichiers
DATA_DIR = "data"
ANSWERS_FILE = os.path.join(DATA_DIR, "answers.pkl")
RESULTS_FILE = os.path.join("main", "optimized_portfolio.pkl")  # Résultats générés par `portfolio_optimizer.py`

# 📌 Vérifier si le dossier `data/` existe, sinon le créer
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 📌 Initialiser `session_state` pour détecter quand l'optimisation est terminée
if "optimization_done" not in st.session_state:
    st.session_state.optimization_done = False

# 📌 Titre de la page
st.title("Portefeuille Optimisé - Questionnaire")

# 📌 Panneau de Configuration (Côté Gauche)
st.sidebar.header("Paramètres Généraux")

# 📌 A. Réglages des Contraintes
st.sidebar.subheader("Réglages des Contraintes")
risk_level = st.sidebar.selectbox("Quel niveau de risque êtes-vous prêt à accepter ?", ["Faible", "Modéré", "Élevé"])
budget = st.sidebar.number_input("Quel est le montant total que vous souhaitez investir ?", min_value=0, value=10000, step=1000)
min_allocation = st.sidebar.slider("Allocation minimale par actif (%)", min_value=0, max_value=100, value=5)
max_allocation = st.sidebar.slider("Allocation maximale par actif (%)", min_value=0, max_value=100, value=50)

# 📌 B. Fréquence de Rebalancement
rebalance_frequency = st.sidebar.radio("À quelle fréquence souhaitez-vous rebalancer votre portefeuille ?", ["Journalier", "Hebdomadaire", "Mensuel", "Pas de rebalancement"])

# 📌 C. Choix des Dividendes
include_dividends = st.sidebar.checkbox("Inclure les dividendes dans les rendements ?")

# 📌 D. Taux sans risque
risk_free_rate = st.sidebar.number_input("Quel taux sans risque voulez-vous utiliser pour le ratio de Sharpe (%) ?", min_value=0.0, value=1.5, step=0.1)

# 📌 Panneau Principal (Côté Droit)
st.header("Sélection des Tickers")

# 📌 Ajout d’un lien pour voir les tickers
st.markdown("**Besoin d'aide pour trouver les tickers ?** 👉 [Voir la liste des principaux tickers]()")

# 📌 Bloc pour entrer les tickers
st.subheader("Entrez les tickers que vous souhaitez inclure dans votre portefeuille")

# Initialisation des session states si besoin
if "tickers" not in st.session_state:
    st.session_state.tickers = [""] * 5  # 5 champs par défaut

# Fonction pour ajouter un nouveau champ de ticker
def add_ticker_block():
    st.session_state.tickers.append("")  # Ajouter un nouveau champ vide

# Afficher les champs dynamiques pour les tickers
for i in range(len(st.session_state.tickers)):
    st.session_state.tickers[i] = st.text_input(f"Ticker {i + 1}", value=st.session_state.tickers[i])

# Bouton pour ajouter un nouveau bloc
if st.button("Add a ticker"):
    add_ticker_block()

# 📌 Méthodes d'Optimisation
st.header("Méthode d'Optimisation")
optimization_method = st.selectbox("Quel type d'optimisation voulez-vous utiliser ?", ["Maximisation du ratio de Sharpe", "Minimisation de la volatilité", "Optimisation pour un rendement cible"])
target_return = None
if optimization_method == "Optimisation pour un rendement cible":
    target_return = st.number_input("Rendement cible (%)", min_value=0.0, value=8.0, step=0.1)

# 📌 🚀 Bouton unique pour valider et lancer l'optimisation
if st.button("🚀 Valider et Lancer l'Optimisation", key="validate_and_run"):
    tickers_selected = [ticker.strip() for ticker in st.session_state.tickers if ticker.strip()]

    if not tickers_selected:
        st.warning("⚠️ Aucun ticker sélectionné. Veuillez entrer au moins un ticker.")
    else:
        st.session_state.validated_tickers = tickers_selected  # Sauvegarde en session

        # 📌 Création du dictionnaire des réponses utilisateur
        answers = {
            "tickers": tickers_selected,
            "risk_level": risk_level,
            "budget": budget,
            "min_allocation": min_allocation,
            "max_allocation": max_allocation,
            "rebalance_frequency": rebalance_frequency,
            "include_dividends": include_dividends,
            "risk_free_rate": risk_free_rate,
            "optimization_method": optimization_method,
            "target_return": target_return
        }

        # ✅ **Sauvegarde dans `data/answers.pkl`**
        with open(ANSWERS_FILE, "wb") as f:
            pickle.dump(answers, f)

        st.success(f"✅ Réponses enregistrées dans '{ANSWERS_FILE}' !")

        # 📌 Lancer `portfolio_optimizer.py` en arrière-plan
        st.write("⏳ Optimisation en cours...")
        subprocess.run(["python", "main/portfolio_optimizer.py"])

        # 📌 Attendre la création du fichier `optimized_portfolio.pkl`
        TIMEOUT = 20  # Maximum 20 secondes d'attente
        elapsed_time = 0

        while not os.path.exists(RESULTS_FILE) and elapsed_time < TIMEOUT:
            time.sleep(0.5)  # Attendre 0.5 seconde avant de revérifier
            elapsed_time += 0.5

        # 📌 Vérification si les résultats sont bien disponibles
        if os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, "rb") as f:
                results = pickle.load(f)

            st.header("📊 Résultats du Portefeuille Optimisé")
            st.write("✅ **Optimisation réussie !**")
            st.write(f"📈 **Rendement attendu :** {results['expected_return']:.2f}%")
            st.write(f"📊 **Volatilité attendue :** {results['expected_volatility']:.2f}%")

            st.subheader("🛠 **Répartition optimale du portefeuille**")
            for asset, amount in results["investment_amounts"].items():
                st.write(f"**{asset}:** {amount:.2f}")

            # 📌 Afficher un tableau avec `st.dataframe`
            df_results = pd.DataFrame.from_dict(results["weights"], orient="index", columns=["Pondération (%)"])
            df_results["Montant Investi (€)"] = df_results.index.map(results["investment_amounts"])
            st.dataframe(df_results.style.format({"Pondération (%)": "{:.2f}%", "Montant Investi (€)": "{:.2f}€"}))

            # 📌 Graphique en camembert
            fig, ax = plt.subplots()
            ax.pie(results["weights"].values(), labels=results["weights"].keys(), autopct="%1.1f%%", startangle=90)
            ax.set_title("📊 Répartition du Portefeuille")
            st.pyplot(fig)

            # 📌 Évolution du portefeuille vs S&P 500
            st.subheader("📈 Évolution en % du Portefeuille vs S&P 500")

            # 📌 Télécharger les données historiques
            tickers = list(results["weights"].keys())
            stock_data = yf.download(tickers + ["SPY"], period="5y")["Close"]

            # 📌 Recalculer l’évolution du portefeuille
            weighted_prices = stock_data[tickers].mul(list(results["weights"].values()), axis=1)
            portfolio_value = weighted_prices.sum(axis=1)

            # 📌 Calcul de l'évolution en pourcentage (%)
            portfolio_returns = (portfolio_value / portfolio_value.iloc[0] - 1) * 100  # 🔥 Conversion en %
            spy_returns = (stock_data["SPY"] / stock_data["SPY"].iloc[0] - 1) * 100  # 🔥 Conversion en %

            # 📌 Tracer le graphique
            fig, ax = plt.subplots()
            ax.plot(portfolio_returns, label="Portefeuille Optimisé", linewidth=2)
            ax.plot(spy_returns, label="S&P 500 (SPY)", linestyle="dashed")

            # 📌 Ajout de titre et labels
            ax.set_title("📈 Évolution du Portefeuille vs S&P 500 en %")
            ax.set_ylabel("Évolution (%)")  # 🔥 Ajout de l’échelle en pourcentage
            ax.legend()

            # 📌 Affichage dans Streamlit
            st.pyplot(fig)

            # 📌 Distribution des rendements journaliers
            st.subheader("📊 Distribution des Rendements Journaliers")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.histplot(portfolio_value.pct_change().dropna(), bins=50, kde=True, ax=ax)
            ax.set_title("📈 Histogramme des Rendements du Portefeuille")
            ax.set_xlabel("Rendement Journalier")
            st.pyplot(fig)

        else:
            st.error("❌ L'optimisation a pris trop de temps ou a échoué. Veuillez réessayer.")