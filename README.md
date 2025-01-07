# Arthurnoo-Markowitz_Portfolio_Sim
Simulateur de Portefeuille avec Optimisation de Markowitz

⚠️ En cours de construction ⚠️

```python
MarkowitzPortfolioSimulator/
│
├── data/                          # Dossier pour les fichiers de données téléchargées ou statiques
│   ├── historical_prices.csv
│   ├── example_returns.csv
│
├── src/                           # Code source principal
│   ├── __init__.py                # Fichier d'initialisation pour le module
│   ├── data_fetcher.py            # Récupération des données financières (yfinance)
│   ├── statistics.py              # Calcul des métriques : rendement, volatilité, covariance
│   ├── optimizer.py               # Optimisation du portefeuille
│   ├── visualization.py           # Graphiques pour la frontière efficiente et autres
│
├── notebooks/                     # Notebooks interactifs pour démonstration
│   ├── example_simulation.ipynb   # Exemple complet d'utilisation du simulateur
│
├── tests/                         # Tests unitaires
│   ├── test_data_fetcher.py
│   ├── test_statistics.py
│   ├── test_optimizer.py
│
├── LICENSE                        # Licence du projet
├── README.md                      # Documentation principale
└── requirements.txt               # Dépendances Python nécessaires

```

La variable `mean_returns` contient les rendements moyens des actifs.
