import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if False:
    pass

bitcoin = pd.read_excel("BTC-EUR.xlsx", index_col="Date", parse_dates=True)
bitcoin.head(10)

plt.figure(figsize=(12,8))
ax = bitcoin["Close"]["2021"].plot()
bitcoin["Close"]["2021"].resample("M").mean().plot(label="moyenne par mois", lw=3, ls=":", alpha=0.8)
bitcoin["Close"]["2021"].resample("W").mean().plot(label="moyenne par semaine", lw=2, ls="--", alpha=0.8)
bitcoin["Close"]["2021"].diff().plot()

ax.set_ylabel("Prix Bitcoin")
ax.yaxis.labelpad = 20  # Espace de 20 points entre le titre et l'axe

plt.legend()
plt.show()

# Aggregate
m = bitcoin["Close"].resample("W").agg(["mean", "std", "min", "max"])
plt.figure(figsize=(12,8))
bx = m["mean"]["2021"].plot(label="moyenne par semaine")

plt.fill_between(m.index, m["max"], m["min"], alpha=0.2, label = "min-max par semaine" )

bx.set_ylabel("Prix Bitcoin")
bx.yaxis.labelpad = 20  # Espace de 20 points entre le titre et l'axe
plt.legend()
plt.show()

# Moving Average and Exponantial Moving Average
plt.figure(figsize=(12,8))
cx = bitcoin.loc["2019-09", "Close"].plot()
# bitcoin.loc["2019-09", "Close"].rolling(window=7, center = True).mean().plot(label="moving average centré", lw=3, ls=":", alpha=0.8)
# bitcoin.loc["2019-09", "Close"].rolling(window=7).mean().plot(label="moving average", lw=3, ls=":", alpha=0.8)

for i in np.arange(0.2, 1, 0.2):
    bitcoin.loc["2019-09", "Close"].ewm(alpha=i).mean().plot(label=f"ewm {i}", lw=3, ls=":", alpha=0.8)

cx.set_ylabel("Prix Bitcoin")
cx.yaxis.labelpad = 20 
plt.legend()
plt.show()

## Ethereum
plt.figure(figsize=(12,8))
ethereum = pd.read_excel("ETH-EUR.xlsx", index_col="Date", parse_dates=True)
dx = ethereum.loc["2019-09", "Close"].plot()

dx.set_ylabel("Prix Ethereum")
dx.yaxis.labelpad = 20  # Espace de 20 points entre le titre et l'axe
plt.legend()
plt.show()

# Merge
btc_eth = pd.merge(bitcoin, ethereum, on="Date", how='inner', suffixes=('_btc',"_eth"))
# btc_eth[["Close_btc", "Close_eth"]].plot(figsize=(12,8))
ex = btc_eth["2019"][["Close_btc", "Close_eth"]].plot(subplots=True, figsize=(12,8))

for ax in ex:
    ax.set_ylabel("Prix Bitcoin")
    ax.yaxis.labelpad = 20
plt.legend()
plt.show

# Corrélation
btc_eth[["Close_btc", "Close_eth"]].corr()






# Turtle strategy

plt.figure(figsize=(12, 8))
fx = bitcoin["Close"]["2019"].plot(label="close")
bitcoin["Close"]["2019"].rolling(window=28).min().plot(label = "min",lw=3, ls=":", alpha=0.8)
bitcoin["Close"]["2019"].rolling(window=28).max().plot(label = "max", lw=3, ls="--", alpha=0.8)

fx.set_ylabel("Prix Ethereum")
fx.yaxis.labelpad = 20  # Espace de 20 points entre le titre et l'axe
plt.legend()
plt.show

# Initialisation des colonnes "Buy" et "Sell"
bitcoin["Buy"] = np.zeros(len(bitcoin))
bitcoin["Sell"] = np.zeros(len(bitcoin))

# Calcul des prix minimum et maximum sur une fenêtre de 28 jours
bitcoin["Rmin"] = bitcoin["Close"].shift(1).rolling(window=28).min()
bitcoin["Rmax"] = bitcoin["Close"].shift(1).rolling(window=28).max()

def boolean_indexing_max(row):
    close = bitcoin.loc[row.name, "Close"]
    if bitcoin.loc[row.name, "Rmax"] < close:
        return 1
    elif row["Rmax"] > close:
        return 0

def boolean_indexing_min(row):
    close = bitcoin.loc[row.name, "Close"]
    if row["Rmin"] < close: 
        return 0
    elif row["Rmin"] > close:
        return -1

# Application des fonctions aux colonnes "Rmax" et "Rmin"
bitcoin["Buy"] = bitcoin.apply(boolean_indexing_max, axis=1)
bitcoin["Sell"] = bitcoin.apply(boolean_indexing_min, axis=1)


# Affichage des signaux d'achat et de vente
plt.figure(figsize=(12, 8))
bitcoin["Buy"]["2019"].plot()
bitcoin["Sell"]["2019"].plot()

plt.legend()
plt.show



print(bitcoin)
