# Arthurnoo-Markowitz_Portfolio_Sim
Simulateur de Portefeuille avec Optimisation de Markowitz

⚠️ En cours de construction ⚠️

```python
MarkowitzPortfolioSimulator/
│
├── data/                          # Dossier pour les fichiers de données téléchargées ou statiques
│   ├── get_data.py                # Récupérer les tickers qui m'intéressent
│
├── src/                           # Code source principal
│   ├── __init__.py                # Fichier d'initialisation pour le module
│   ├── data_fetcher.py            # Récupération des données financières (yfinance)
│   ├── statistics.py              # Calcul des métriques : rendement, volatilité, covariance
│   ├── optimizer.py               # Optimisation du portefeuille
│   ├── visualization.py           # Graphiques pour la frontière efficiente et autres
│   ├── streamlit_app.py           # Application interactive Streamlit
│
├── notebooks/                     # Notebooks interactifs pour démonstration
│   ├── example_simulation.ipynb   # Exemple complet d'utilisation du simulateur
│
├── tests/                         # Tests unitaires
│   ├── test_data_fetcher.py       # Tests pour la récupération des données
│   ├── test_statistics.py         # Tests pour les calculs statistiques
│   ├── test_optimizer.py          # Tests pour l'optimisation
│   ├── test_streamlit_app.py      # Tests pour l'application Streamlit
│
├── LICENSE                        # Licence du projet
├── README.md                      # Documentation principale
├── requirements.txt               # Dépendances Python nécessaires
└── .streamlit/                    # Configuration pour Streamlit
    ├── config.toml                # Paramètres de configuration (ex : thème, port)
```

Voici à quoi servent chacune des pages :
1. `src/data_fetcher.py` :
  - Récupère les données financières depuis des sources comme yfinance.
  - Offre des fonctionnalités pour télécharger, sauvegarder, et charger des données.
2. `src/statistics.py` :
  - Calcule les rendements moyens, la matrice de covariance, et les statistiques des portefeuilles.
3. `src/optimizer.py` :
  - Implémente les algorithmes d’optimisation pour minimiser le risque ou maximiser le rendement/ration de Sharpe.
4. `src/visualisation.py`:
  - Gère les graphiques interactifs pour visualiser la frontière efficiente, les poids des portefeuilles, etc.
5. `src/streamlit_app.py` :
  - Application interactive Streamlit permettant :
    - De poser des questions sur le profil de risque.
    - De configurer les paramètres d’optimisation.
    - De visualiser les résultats.
------
6. `notebooks/example_simulation.ipynb`:
  - Montre comment récupérer des données, calculer les rendements, optimiser un portefeuille, et afficher les graphiques.
------
7. `tests/test_data_fetcher.py` :
  - Vérifie que les données sont correctement récupérées et formatées.
8. `tests/test_statistics.py` :
  - Teste les calculs des métriques (rendements, volatilité, etc.).
9. `tests/test_optimizer.py` :
  - Vérifie la convergence et la validité des résultats de l’optimisation.
10. `tests/test_streamlit_app.py` :
  - Valide les entrées utilisateur et les réponses de l’application Streamlit.
------
11. `requirements.txt` :
  - Contient la liste des dépendances Python nécessaires :yfinance, numpy, pandas, scipy, matplotlib, streamlit.
12. `.streamlit/` :
  - Configurer l'apparence de l'interface streamlit.
