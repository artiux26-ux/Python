# PROGETTO: PREVISIONE VENDITE (VERSIONE SEMPLICE)

import pandas as pd

# CREAZIONE DATASET 

data = {
    'Data': ['10.04.26', '12.04.26', '12.04.26', '12.04.26'],
    'Prodotto': ['A', 'B', 'C', 'D'],
    'Vendite': [10, 6, None, 8],
    'Prezzo': [2.5, 3.0, 4.0, 4.5]
}

df = pd.DataFrame(data)

df.to_csv('vendite.csv', index=False)

# PARTE 1 - CARICAMENTO DATI

# 1.1 Leggere il dataset
df = pd.read_csv('vendite.csv')

# 2. Esplorazione iniziale
print("Prime righe:")
print(df.head())

print("\nInfo dataset:")
print(df.info())

print("\nStatistiche descrittive:")
print(df.describe())

# PARTE 2 - PULIZIA DATI

# 3. Gestione valori mancanti

df['Vendite'] = df['Vendite'].fillna(0)

# Se il prezzo esiste, riempi con la media
if 'Prezzo' in df.columns:
    df['Prezzo'] = df['Prezzo'].fillna(df['Prezzo'].mean())

# 4. Rimuovere duplicati
df = df.drop_duplicates()

# 5. Correzione tipi di dato

df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

df['Vendite'] = pd.to_numeric(df['Vendite'], errors='coerce')

# PARTE 3 - ANALISI ESPLORATIVA

# 6. Vendite totali per prodotto
vendite_per_prodotto = df.groupby('Prodotto')['Vendite'].sum()
print("\nVendite totali per prodotto:")
print(vendite_per_prodotto)

# 7. Prodotto più e meno venduto
prodotto_top = vendite_per_prodotto.idxmax()
prodotto_bottom = vendite_per_prodotto.idxmin()

print("\nProdotto più venduto:", prodotto_top)
print("Prodotto meno venduto:", prodotto_bottom)

# 8. Vendite medie giornaliere
vendite_giornaliere = df.groupby('Data')['Vendite'].sum()
media_giornaliera = vendite_giornaliere.mean()

print("\nVendite medie giornaliere:", media_giornaliera)

