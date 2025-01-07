# Arthurnoo-Markowitz_Portfolio_Sim
Simulateur de Portefeuille avec Optimisation de Markowitz

⚠️ En cours de construction ⚠️

```python
import yfinance as yf

# Télécharger les prix historiques
data = yf.download("AAPL", start="2020-01-01", end="2022-12-31")
print(data.head())
