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
Pour comprendre son fonctionnement, consultez le notebook : `portfolio_optimizer_tutorial.ipynb`
Ce fichier est un point de départ pour comprendre comment utiliser le projet dans son intégralité.

---

## Interface Streamlit

Pour rendre l'utilisation de l'outil plus intuitive, nous avons développé une interface utilisateur avec Streamlit. Elle permet de configurer son portefeuille, de lancer l’optimisation et de visualiser les résultats en quelques clics, sans avoir à écrire une seule ligne de code Python.

Voici à quoi ressemble l’interface utilisateur :

![Question py](https://github.com/user-attachments/assets/5f745dc6-961f-449d-b5f9-fd885a9fbeb0)

🛠 Panneau de configuration (côté gauche)
Ce panneau permet de configurer les paramètres d'investissement avant de lancer l'optimisation.

- Niveau de risque : Sélectionnez votre appétence au risque (Faible, Modéré, Élevé).
- Budget total : Indiquez le montant total que vous souhaitez investir.
- Contraintes d’allocation : Fixez les bornes de répartition pour chaque actif (% minimum et % maximum).
- Fréquence de rebalancement : Déterminez si le portefeuille doit être ajusté automatiquement (quotidien, hebdomadaire, mensuel, ou pas de rebalancement).
- Prise en compte des dividendes : Activez ou désactivez cette option.
- Taux sans risque : Définissez un taux de référence utilisé pour le ratio de Sharpe.

📍 Panneau principal (côté droit)
Ce panneau est dédié à la sélection des actifs et à l'affichage des résultats.

- Sélection des actifs

Entrée des tickers : Saisissez les symboles boursiers des actifs à inclure dans votre portefeuille.
- Ajout dynamique : Utilisez le bouton "Add a ticker" pour ajouter de nouveaux actifs.
- Assistance : Un lien vous permet d'afficher une liste des principaux tickers.
- Méthode d’optimisation : Choisissez la stratégie d’optimisation :
  - Maximisation du ratio de Sharpe (meilleur rendement ajusté au risque).
  - Minimisation de la volatilité (portefeuille le plus stable).
  - Optimisation pour un rendement cible (ajustement pour atteindre un objectif spécifique).
- Rendement cible (si sélectionné) : Indiquez votre objectif de rendement annuel.


Bouton "Valider et Lancer l’Optimisation" : Une fois les paramètres définis, cliquez pour lancer l’algorithme d’optimisation.
Exécution automatique : Le système récupère les données financières, applique les calculs et génère les résultats.

📊 Affichage des résultats

- Résumé des performances :
- Rendement attendu (%)
- Volatilité attendue (%)
- Répartition optimale :
Affichage des poids optimaux pour chaque actif dans le portefeuille.
- Évolution du portefeuille vs S&P 500 :
Un graphique interactif compare la performance passée du portefeuille optimisé face au S&P 500.
- Montants investis :
Détail du montant alloué à chaque actif en fonction du budget initial.

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
