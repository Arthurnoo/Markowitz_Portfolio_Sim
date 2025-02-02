import os
import pickle
import subprocess
import sys

# Vérifier si Streamlit est installé, sinon l'installer
try:
    import streamlit as st
except ImportError:
    print("Streamlit n'est pas installé. Installation en cours...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])

# 📌 Définir le chemin du fichier
DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "validated_tickers.pkl")

# Vérifier si le dossier "data" existe, sinon le créer
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 📌 Titre de la page
st.title("Portefeuille Optimisé - Questionnaire")

# 📌 Panneau de Configuration (Côté Gauche)
st.sidebar.header("Paramètres Généraux")

# A. Réglages des Contraintes
st.sidebar.subheader("Réglages des Contraintes")
risk_level = st.sidebar.selectbox(
    "Quel niveau de risque êtes-vous prêt à accepter ?",
    ["Faible", "Modéré", "Élevé"]
)
budget = st.sidebar.number_input(
    "Quel est le montant total que vous souhaitez investir ?",
    min_value=0, value=10000, step=1000
)
min_allocation = st.sidebar.slider(
    "Allocation minimale par actif (%)", min_value=0, max_value=100, value=5
)
max_allocation = st.sidebar.slider(
    "Allocation maximale par actif (%)", min_value=0, max_value=100, value=50
)

# B. Fréquence de Rebalancement
rebalance_frequency = st.sidebar.radio(
    "À quelle fréquence souhaitez-vous rebalancer votre portefeuille ?",
    ["Journalier", "Hebdomadaire", "Mensuel", "Pas de rebalancement"]
)

# C. Choix des Dividendes
include_dividends = st.sidebar.checkbox("Inclure les dividendes dans les rendements ?")

# D. Taux sans risque
risk_free_rate = st.sidebar.number_input(
    "Quel taux sans risque voulez-vous utiliser pour le ratio de Sharpe (%) ?",
    min_value=0.0, value=1.5, step=0.1
)

# 📌 Panneau Principal (Côté Droit)
st.header("Sélection des Tickers")

# Ajouter un lien pour voir les tickers
st.markdown(
    """
    **Besoin d'aide pour trouver les tickers ?** 
    👉 [Voir la liste des principaux tickers]()
    """
)

# 📌 Bloc pour entrer les tickers
st.subheader("Entrez les tickers que vous souhaitez inclure dans votre portefeuille")

# Initialisation des session states si besoin
if "tickers" not in st.session_state:
    st.session_state.tickers = [""] * 5  # 5 blocs par défaut

# Fonction pour ajouter un nouveau champ de ticker
def add_ticker_block():
    st.session_state.tickers.append("")  # Ajouter un nouveau champ vide

# Afficher les champs dynamiques pour les tickers
for i in range(len(st.session_state.tickers)):
    st.session_state.tickers[i] = st.text_input(f"Ticker {i + 1}", value=st.session_state.tickers[i])

# Bouton pour ajouter un nouveau bloc
if st.button("Add a ticker"):
    add_ticker_block()

# 🚀 **Bouton unique pour valider et enregistrer les tickers**
if st.button("✅ Valider les tickers", key="validate_tickers_button"):
    tickers_selected = [ticker.strip() for ticker in st.session_state.tickers if ticker.strip()]
    
    if not tickers_selected:
        st.warning("⚠️ Aucun ticker sélectionné. Veuillez entrer au moins un ticker.")
    else:
        st.session_state.validated_tickers = tickers_selected  # Sauvegarde en session

        # ✅ **Sauvegarde dans `data/validated_tickers.pkl`**
        with open(FILE_PATH, "wb") as f:
            pickle.dump(tickers_selected, f)

        st.success(f"✅ Tickers validés et enregistrés dans '{FILE_PATH}'.")
        st.write("Tickers validés :", tickers_selected)

# 📌 Méthodes d'Optimisation
st.header("Méthode d'Optimisation")
optimization_method = st.selectbox(
    "Quel type d'optimisation voulez-vous utiliser ?",
    ["Maximisation du ratio de Sharpe", "Minimisation de la volatilité", "Rendement cible"]
)
target_return = None
if optimization_method == "Rendement cible":
    target_return = st.number_input("Rendement cible (%)", min_value=0.0, value=8.0, step=0.1)

# 📌 Bouton pour lancer l'optimisation
if st.button("Lancer l'optimisation"):
    st.write("L'optimisation est en cours...")