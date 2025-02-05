⚠️ En cours de construction ⚠️

# Simulateur de Portfolio suivant la théorie d'Optimisation de Markowitz

## Overview

Ce projet permet d’optimiser un portefeuille d’investissement en utilisant la **théorie de Markowitz**.  
Grâce à une **interface interactive en Streamlit**, l’utilisateur peut :  
- Sélectionner ses actifs  
- Définir son niveau de risque et ses contraintes  
- Lancer une optimisation du portefeuille sous plusieurs méthodes  
- Visualiser les performances passées et comparer avec le S&P 500  

---

## Fonctionnalités principales
✔️ **Optimisation selon différentes stratégies** :  
- Maximisation du ratio de Sharpe  
- Minimisation de la volatilité  
- Optimisation pour un rendement cible  

✔️ **Gestion avancée des contraintes** :  
- Allocation minimale et maximale par actif  
- Intégration d’un taux sans risque  
- Fréquence de rebalancement configurable  

✔️ **Analyse et visualisation** :  
- Calcul des rendements, volatilités et corrélations  
- Comparaison avec le S&P 500  
- Représentation graphique de l’évolution du portefeuille  

✔️ **Tests automatisés** :  
- Simulation avec des portefeuilles fictifs  
- Vérification de la robustesse du modèle
---

## Installation

Importer le répertoire :
```bash
git clone https://github.com/Arthurnoo/Markowitz_Portfolio_Sim.git
cd Markowitz_Portfolio_Sim
```
Installer les dépendances :
```bash
pip install -r requirements.txt
```
---

## Structure

```python
MarkowitzPortfolioSimulator/
│
├── data/                                 # Dossier concernant la compréhension et la récupération de la data
│   ├── __init__.py                            # Fichier d'initialisation pour le module
│   ├── answer.pkl                             # Fichier des réponses de l'utilisateur dans interface.py
│   ├── get_data.py                            # Récupérer les tickers du S&P 500
│   ├── interface.py                           # Page internet streamlit pour récupérer les informations de l'utilisateur, et afficher les résultats
│   ├── tickers_list.py                        # Liste des principaux tickers (aide pour les utilisateurs)
│   ├── yfinance.ipynb                         # Notebook pour la compréhension basique de yfinance
│
├── main/                                 # Notebooks interactifs pour démonstration
│   ├── __init__.py                            # Fichier d'initialisation pour le module
│   ├── optimized_portfolio.pkl                # Fichier avec les données finales pour l'exporter dans interface.py
│   ├── portfolio_optimizer.py                 # Optimisation des données sous contraintes
│   ├── statistics.py                          # Calcul des statistiques basiques des tickers (rendements moyens, volatilités, matrice de corrélation)
│
├── tests/                                # Tests unitaires
│   ├── test_1.py                              # Simulation de réponse utilisateur 1 (5 tickers)
│   ├── test_2.py                              # Simulation de réponse utilisateur 2 (10 tickers)
│   ├── test_3.py                              # Simulation de réponse utilisateur 3 (20 tickers)
│   ├── run_tests.py                           # Faire tourner les fichiers de tests et vérifier que tout fonctionne
│
├── portfolio_optimizer_tutorial.ipynb    # Notebook guide complet pour l'utilisateur
│
├── LICENSE                               # Licence du projet
├── README.md                             # Documentation principale
└── requirements.txt                      # Dépendances Python nécessaires
```

---

## Utilisation

Le projet permet d’optimiser un portefeuille d’investissement sous contraintes.
Pour comprendre son fonctionnement, consultez le notebook : portfolio_optimizer_tutorial.ipynb
Ce fichier est un point de départ pour comprendre comment utiliser le projet dans son intégralité.

---

## Interface Streamlit

Pour rendre l’utilisation du framework plus accessible, nous fournissons une **interface utilisateur** développée avec [Streamlit](https://streamlit.io/). Elle vous permet de réaliser et de visualiser vos backtests sans avoir à écrire de code Python. Voici ce à quoi ressemble l’interface utilisateur :

![Interface Streamlit](images/streamlit_interface.png)

- **Panneau de configuration (côté gauche)** :
  - Réglage des paramètres financiers (coûts de transaction, slippage, taux sans risque, etc.).
  - Choix de la fréquence de rebalancement (journalier, hebdomadaire, mensuel...).
  - Sélection du schéma de pondération (EqualWeight, MarketCapWeight...).
  - Définition d’un index de “special start” pour ignorer un certain nombre de lignes de données initiales.
  - Choix de la bibliothèque de visualisation (matplotlib, seaborn, plotly…).
  - Activations optionnelles (Vol Target, comparaison de stratégies, etc.).

- **Panneau principal (côté droit)** :
  - Téléversement de fichiers de données (formats CSV, Parquet...).
  - Sélection de la stratégie (Moyenne Mobile, MinVariance, etc.).
  - Configuration des paramètres spécifiques à la stratégie (ex. taille de fenêtres pour une stratégie de moyennes mobiles).
  - Bouton d’exécution du backtest et affichage des résultats (statistiques, graphiques interactifs).

Pour lancer l'interface graphique Streamlit, exécutez la commande suivante depuis le terminal :

```bash
streamlit run data/interface.py
```

---
## Auteur

**Arthur NEAU**

Sous la supervision de **M. Rémi Genet**.

---

## Licence

Ce projet est sous licence MIT.
