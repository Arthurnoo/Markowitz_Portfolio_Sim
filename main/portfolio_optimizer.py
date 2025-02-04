import os
import pickle
import numpy as np
import scipy.optimize as sco
import sys

# 📌 Importer les statistiques calculées (rendements, volatilité, covariance)
from statistics import analyze_portfolio

# 📌 Définir le chemin du fichier contenant les réponses de l'utilisateur
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
ANSWER_PATH = os.path.join(DATA_DIR, "answers.pkl")
ANSWER_DIR = os.path.join(BASE_DIR, "../main")
RESULTS_PATH = os.path.join(ANSWER_DIR, "optimized_portfolio.pkl")  # 📌 Fichier pour sauvegarder les résultats

# 📌 Charger les réponses de l'utilisateur
def load_user_preferences():
    """
    Charge les préférences de l'utilisateur enregistrées dans `answers.pkl`.

    Returns:
        dict: Contient les paramètres d'optimisation.
    """
    try:
        with open(ANSWER_PATH, "rb") as f:
            preferences = pickle.load(f)
        return preferences
    except FileNotFoundError:
        print(f"❌ Fichier introuvable : '{ANSWER_PATH}'")
        return None

# 📌 Charger les préférences utilisateur
user_preferences = load_user_preferences()
if not user_preferences:
    print("❌ Impossible de charger les préférences utilisateur.")
    sys.exit(1)

# 📌 Extraire les paramètres d'optimisation
risk_level = user_preferences["risk_level"]
budget = user_preferences["budget"]
min_allocation = user_preferences["min_allocation"] / 100
max_allocation = user_preferences["max_allocation"] / 100
risk_free_rate = user_preferences["risk_free_rate"] / 100
optimization_method = user_preferences["optimization_method"]

# 📌 Charger les statistiques des actifs
portfolio_stats = analyze_portfolio()
if not portfolio_stats:
    print("❌ Échec de la récupération des statistiques.")
    sys.exit(1)

# 📌 Extraire les statistiques
mean_returns = portfolio_stats["annualized_returns"]
cov_matrix = portfolio_stats["covariance_matrix"]

# 📌 Nombre d'actifs
num_assets = len(mean_returns)

# 📌 Contraintes d’allocation (min/max)
bounds = tuple((min_allocation, max_allocation) for _ in range(num_assets))
constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}  # Somme des poids = 1

# 📌 Fonction à optimiser selon le choix de l'utilisateur
def neg_sharpe_ratio(weights):
    """ Fonction à minimiser pour maximiser le ratio de Sharpe """
    port_return = np.dot(weights, mean_returns)
    port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return - (port_return - risk_free_rate) / port_volatility  # Maximisation du Sharpe

def min_volatility(weights):
    """ Fonction à minimiser pour minimiser la volatilité """
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

def target_return_constraint(weights, target_return):
    """ Contrainte : atteindre un rendement cible """
    return np.dot(weights, mean_returns) - target_return

# 📌 Vérification si le rendement cible est atteignable
max_possible_return = np.max(mean_returns) * 252  # Rendement annuel max atteignable
min_possible_return = np.min(mean_returns) * 252  # Rendement annuel min atteignable

if optimization_method == "Optimisation pour un rendement cible":
    target_return = user_preferences["target_return"] / 100  # Convertir en fraction

    if target_return > max_possible_return:
        print(f"❌ Impossible d'atteindre un rendement cible de {target_return:.2f}%.")
        print(f"📌 Le rendement max possible avec ces actifs est {max_possible_return:.2f}%.")
        print("💡 Ajustement automatique du rendement cible au rendement maximal atteignable.")
        target_return = max_possible_return  # Ajustement automatique

    if target_return < min_possible_return:
        print(f"❌ Impossible d'atteindre un rendement cible de {target_return*100:.2f}%.")
        print(f"📌 Le rendement minimum réalisable avec ces actifs est {min_possible_return:.2f}%.")
        print("💡 Ajustement automatique du rendement cible au rendement minimum atteignable.")
        target_return = min_possible_return  # Ajustement automatique

# 📌 Optimisation en fonction du choix utilisateur
if optimization_method == "Maximisation du ratio de Sharpe":
    result = sco.minimize(neg_sharpe_ratio, np.ones(num_assets) / num_assets,
                          method="SLSQP", bounds=bounds, constraints=constraints)

elif optimization_method == "Minimisation de la volatilité":
    result = sco.minimize(min_volatility, np.ones(num_assets) / num_assets,
                          method="SLSQP", bounds=bounds, constraints=constraints)

elif optimization_method == "Optimisation pour un rendement cible":
    new_constraints = [constraints, {"type": "eq", "fun": lambda w: target_return_constraint(w, target_return)}]
    result = sco.minimize(min_volatility, np.ones(num_assets) / num_assets,
                          method="SLSQP", bounds=bounds, constraints=new_constraints)

    # 📌 Si l'optimisation échoue, essayer d'élargir les bornes de l'allocation
    if not result.success:
        print("⚠️ L'optimisation a échoué avec les contraintes actuelles.")
        print("🔄 Réduction des contraintes d'allocation et nouvel essai...")

        new_min_allocation = min_allocation / 2  # Diminuer la contrainte min
        bounds = tuple((new_min_allocation, 1) for _ in range(num_assets))

        result = sco.minimize(min_volatility, np.ones(num_assets) / num_assets,
                              method="SLSQP", bounds=bounds, constraints=new_constraints)

# 📌 Vérification de la réussite de l'optimisation
if not result.success:
    print(f"❌ Échec de l'optimisation même après relaxation des contraintes : {result.message}")
    print("💡 Essayez de modifier les actifs sélectionnés ou d'assouplir les contraintes d'allocation.")
    sys.exit(1)

# 📌 Résultats de l'optimisation
optimal_weights = result.x
expected_return = np.dot(optimal_weights, mean_returns)
expected_volatility = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights)))

# 📌 Calculer les montants investis en fonction du budget total
investment_amounts = optimal_weights * budget

# 📌 Création du dictionnaire des résultats
optimized_results = {
    "expected_return": expected_return * 100,
    "expected_volatility": expected_volatility * 100,
    "weights": {asset: weight * 100 for asset, weight in zip(mean_returns.index, optimal_weights)},
    "investment_amounts": {asset: amount for asset, amount in zip(mean_returns.index, investment_amounts)}
}

# 📌 Sauvegarde des résultats dans un fichier pour `view_results.py`
with open(RESULTS_PATH, "wb") as f:
    pickle.dump(optimized_results, f)

# 📌 Affichage des résultats
print("\n✅ **Optimisation réussie !**")
print(f"📈 **Rendement attendu :** {optimized_results['expected_return']:.2f}%")
print(f"📊 **Volatilité attendue :** {optimized_results['expected_volatility']:.2f}%\n")

print("🛠 **Répartition optimale du portefeuille :**")
for asset, weight in optimized_results["weights"].items():
    print(f"{asset}: {weight:.2f}%")

print("\n💰 **Montants investis :**")
for asset, amount in optimized_results["investment_amounts"].items():
    print(f"{asset}: {amount:.2f}€")

print(f"\n✅ Résultats sauvegardés dans `{RESULTS_PATH}`")