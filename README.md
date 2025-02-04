# Arthurnoo-Markowitz_Portfolio_Sim
Simulateur de Portefeuille avec Optimisation de Markowitz

⚠️ En cours de construction ⚠️

```python
MarkowitzPortfolioSimulator/
│
├── data/                     # Dossier concernant la compréhension et la récupération de la data
│   ├── __init__.py                # Fichier d'initialisation pour le module
│   ├── answer.pkl                 # Fichier des réponses de l'utilisateur dans interface.py
│   ├── get_data.py                # Récupérer les tickers du S&P 500
│   ├── interface.py               # Page internet streamlit pour récupérer les informations de l'utilisateur, et afficher les résultats
│   ├── tickers_list.py            # Liste des principaux tickers (aide pour les utilisateurs)
│   ├── yfinance.ipynb             # Notebook pour la compréhension basique de yfinance
│
├── main/                     # Notebooks interactifs pour démonstration
│   ├── __init__.py                # Fichier d'initialisation pour le module
│   ├── optimized_portfolio.pkl    # Fichier avec les données finales pour l'exporter dans interface.py
│   ├── portfolio_optimizer.py     # Optimisation des données sous contraintes
│   ├── statistics.py              # Calcul des statistiques basiques des tickers (rendements moyens, volatilités, matrice de corrélation)
│
├── tests/                    # Tests unitaires
│   ├── test_1.py                  # Simulation de réponse utilisateur 1 (5 tickers)
│   ├── test_2.py                  # Simulation de réponse utilisateur 2 (10 tickers)
│   ├── test_3.py                  # Simulation de réponse utilisateur 3 (20 tickers)
│   ├── run_tests.py               # Faire tourner les fichiers de tests et vérifier que tout fonctionne
│
├── LICENSE                        # Licence du projet
├── README.md                      # Documentation principale
└── requirements.txt               # Dépendances Python nécessaires
```
