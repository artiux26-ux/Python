import pandas as pd
import numpy as np
import json

np.random.seed(42)


# PARTE 1 - CREAZIONE DATI


# ORDINI (100.000 righe)
n_ordini = 100000
ordini = pd.DataFrame({
    "ClienteID": np.random.randint(1, 5001, n_ordini),
    "ProdottoID": np.random.randint(1, 21, n_ordini),
    "Quantità": np.random.randint(1, 5, n_ordini),
    "DataOrdine": pd.to_datetime("2024-01-01") + pd.to_timedelta(np.random.randint(0, 365, n_ordini), unit='D')
})
ordini.to_csv("ordini.csv", index=False)

# PRODOTTI (20 prodotti)
prodotti = []
for i in range(1, 21):
    prodotti.append({
        "ProdottoID": i,
        "Categoria": f"Categoria_{np.random.randint(1,5)}",
        "Fornitore": f"Fornitore_{np.random.randint(1,4)}",
        "Prezzo": round(np.random.uniform(5, 100), 2)
    })

with open("prodotti.json", "w") as f:
    json.dump(prodotti, f)

# CLIENTI (5000 clienti)
clienti = pd.DataFrame({
    "ClienteID": range(1, 5001),
    "Regione": np.random.choice(["Nord", "Centro", "Sud"], 5000),
    "Segmento": np.random.choice(["Retail", "Business"], 5000)
})
clienti.to_csv("clienti.csv", index=False)

# PARTE 2 - MERGE DATI

ordini = pd.read_csv("ordini.csv")
prodotti = pd.read_json("prodotti.json")
clienti = pd.read_csv("clienti.csv")

df = ordini.merge(prodotti, on="ProdottoID")
df = df.merge(clienti, on="ClienteID")

# PARTE 3 - OTTIMIZZAZIONE

df["ClienteID"] = df["ClienteID"].astype("int32")
df["ProdottoID"] = df["ProdottoID"].astype("int8")
df["Quantità"] = df["Quantità"].astype("int8")

df["Categoria"] = df["Categoria"].astype("category")
df["Fornitore"] = df["Fornitore"].astype("category")
df["Regione"] = df["Regione"].astype("category")
df["Segmento"] = df["Segmento"].astype("category")

print(df.info(memory_usage="deep"))

# PARTE 4 - CALCOLI E FILTRI

df["ValoreTotale"] = df["Prezzo"] * df["Quantità"]

df_filtrato = df[df["ValoreTotale"] > 100]

print(df_filtrato.head())
print("Numero ordini filtrati:", len(df_filtrato))