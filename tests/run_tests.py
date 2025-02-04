import os
import importlib
import sys
import subprocess
import pickle

# 📌 Définition des chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Dossier `tests`
MAIN_DIR = os.path.join(BASE_DIR, "../main")  # Dossier `main`
ANSWERS_FILE = os.path.join(BASE_DIR, "../data/answers.pkl")  # Fichier temporaire des réponses
RESULTS_FILE = os.path.join(MAIN_DIR, "optimized_portfolio.pkl")  # Fichier des résultats

# 📌 Ajouter `main/` au PATH pour pouvoir importer les modules
sys.path.append(BASE_DIR)  # Ajouter le dossier `tests` au path Python

def run_test_scenario(test_file):
    """
    Exécute un scénario de test complet :
    1. Charge les réponses utilisateur depuis un fichier Python (.py).
    2. Exécute `statistics.py` pour récupérer les données financières.
    3. Exécute `portfolio_optimizer.py` pour optimiser le portefeuille.
    4. Retourne les résultats optimisés.

    Args:
        test_file (str): Nom du fichier de test (ex: "test_case_1")

    Returns:
        dict: Résultats optimisés du portefeuille.
    """
    # 📌 Vérifier si le fichier existe
    test_module_path = f"{test_file}"
    try:
        test_module = importlib.import_module(test_module_path)
    except ModuleNotFoundError:
        print(f"❌ Le fichier de test '{test_file}.py' n'existe pas dans `tests/`.")
        return None

    # 📌 Récupérer les réponses du fichier de test
    answers = test_module.answers
    print("\n✅ Paramètres du test chargés depuis :", test_file)
    for key, value in answers.items():
        print(f"{key}: {value}")

    # 📌 Sauvegarder les réponses dans `answers.pkl`
    with open(ANSWERS_FILE, "wb") as f:
        pickle.dump(answers, f)

    print("\n📁 ✅ Fichier `answers.pkl` mis à jour.")

    # 📌 Exécuter `statistics.py` pour récupérer les données financières
    print("\n⏳ Exécution de `statistics.py` pour récupérer les données financières...")
    subprocess.run(["python", os.path.join(MAIN_DIR, "statistics.py")])

    # 📌 Exécuter `portfolio_optimizer.py` pour optimiser le portefeuille
    print("\n⏳ Exécution de `portfolio_optimizer.py` pour optimiser le portefeuille...")
    subprocess.run(["python", os.path.join(MAIN_DIR, "portfolio_optimizer.py")])

    # 📌 Vérification des résultats
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "rb") as f:
            results = pickle.load(f)

        print("\n📊 ✅ **Résultats du Portefeuille Optimisé**")
        print(f"📈 **Rendement attendu :** {results['expected_return']:.2f}%")
        print(f"📊 **Volatilité attendue :** {results['expected_volatility']:.2f}%\n")

        print("🛠 **Répartition optimale du portefeuille :**")
        for asset, weight in results["weights"].items():
            print(f"{asset}: {weight:.2f}%")

        print("\n💰 **Montants investis :**")
        for asset, amount in results["investment_amounts"].items():
            print(f"{asset}: {amount:.2f}€")

        return results
    else:
        print("❌ Erreur : Aucun fichier de résultats trouvé.")
        return None

# 📌 Exécuter le script si lancé directement
if __name__ == "__main__":
    print("\n📢 Sélectionnez un test à exécuter :")
    print("1 - Test avec 5 tickers connus (test_1)")
    print("2 - Test avec 10 tickers moins connus (test_2)")
    print("3 - Test avec 20 tickers rares (test_3)")
    
    choice = input("\n🔹 Entrez le numéro du test à exécuter : ")

    test_cases = {
        "1": "test_1",
        "2": "test_2",
        "3": "test_3"
    }

    if choice in test_cases:
        selected_test = test_cases[choice]
        print(f"\n🎯 Exécution du test : {selected_test}.py\n")
        run_test_scenario(selected_test)
    else:
        print("❌ Choix invalide. Veuillez sélectionner 1, 2 ou 3.")