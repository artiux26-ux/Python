import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# PARTE 1 – Creazione Dataset

np.random.seed(42)

date = pd.date_range(start="2026-09-01", periods=30)

negozi = ["Milano", "Roma", "Napoli", "Torino", "Bologna"]
prodotti = ["Smartphone", "Laptop", "TV", "Tablet", "Smartwatch"]

data = {
    "Data": np.random.choice(date, 30),
    "Negozio": np.random.choice(negozi, 30),
    "Prodotto": np.random.choice(prodotti, 30),
    "Quantità": np.random.randint(1, 10, 30),
    "Prezzo_unitario": np.round(np.random.uniform(200, 1200, 30), 2)
}

df = pd.DataFrame(data)

# salva il CSV richiesto
df.to_csv("vendite.csv", index=False)

print("File vendite.csv creato\n")

# PARTE 2 – Importazione con Pandas


df = pd.read_csv("vendite.csv")

print("Prime 5 righe:")
print(df.head())

print("\nShape (righe, colonne):")
print(df.shape)

print("\nInfo DataFrame:")
print(df.info())


# PARTE 3 – Elaborazioni con Pandas

df["Incasso"] = df["Quantità"] * df["Prezzo_unitario"]

incasso_totale = df["Incasso"].sum()
incasso_medio_negozio = df.groupby("Negozio")["Incasso"].mean()

top_prodotti = df.groupby("Prodotto")["Quantità"].sum().sort_values(ascending=False).head(3)

incasso_medio_gruppo = df.groupby(["Negozio", "Prodotto"])["Incasso"].mean()

print("\nIncasso totale:", incasso_totale)

print("\nIncasso medio per negozio:")
print(incasso_medio_negozio)

print("\nTop 3 prodotti più venduti:")
print(top_prodotti)

print("\nIncasso medio per Negozio e Prodotto:")
print(incasso_medio_gruppo)


# PARTE 4 – Uso di NumPy

q = df["Quantità"].to_numpy()

media = np.mean(q)
minimo = np.min(q)
massimo = np.max(q)
dev_std = np.std(q)

percentuale_sopra_media = np.sum(q > media) / len(q) * 100

print("\nStatistiche quantità vendute:")
print("Media:", media)
print("Minimo:", minimo)
print("Massimo:", massimo)
print("Deviazione standard:", dev_std)
print("Percentuale sopra la media:", percentuale_sopra_media)

# array 2D con quantità e prezzo
array_np = df[["Quantità", "Prezzo_unitario"]].to_numpy()

incassi_np = array_np[:,0] * array_np[:,1]

print("\nConfronto incassi NumPy vs DataFrame:")
print("Incassi NumPy (prime 5):", incassi_np[:5])
print("Incassi DataFrame (prime 5):", df["Incasso"].values[:5])


# PARTE 5 – Grafici Matplotlib


# grafico a barre incasso per negozio
plt.figure()
df.groupby("Negozio")["Incasso"].sum().plot(kind="bar")
plt.title("Incasso totale per negozio")
plt.ylabel("Incasso (€)")
plt.show()

# grafico a torta incassi per prodotto
plt.figure()
df.groupby("Prodotto")["Incasso"].sum().plot(kind="pie", autopct="%1.1f%%")
plt.title("Percentuale incassi per prodotto")
plt.ylabel("")
plt.show()

# grafico a linee andamento giornaliero
df["Data"] = pd.to_datetime(df["Data"])

incasso_giornaliero = df.groupby("Data")["Incasso"].sum()

plt.figure()
incasso_giornaliero.plot(kind="line")
plt.title("Andamento giornaliero incassi")
plt.ylabel("Incasso (€)")
plt.xlabel("Data")
plt.show()

# PARTE 6 – Analisi Avanzata

categorie = {
    "Smartphone": "Informatica",
    "Laptop": "Informatica",
    "Tablet": "Informatica",
    "TV": "Elettrodomestici",
    "Smartwatch": "Accessori"
}

df["Categoria"] = df["Prodotto"].map(categorie)

incasso_categoria = df.groupby("Categoria")["Incasso"].sum()
quantita_media_categoria = df.groupby("Categoria")["Quantità"].mean()

print("\nIncasso totale per categoria:")
print(incasso_categoria)

print("\nQuantità media venduta per categoria:")
print(quantita_media_categoria)

# salva nuovo file
df.to_csv("vendite_analizzate.csv", index=False)

print("\nFile vendite_analizzate.csv salvato.")