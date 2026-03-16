import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# PARTE 1 – Variabili

nome = "Aldo Baglio"
eta = 40
saldo = 2910.75
vip = True

destinazioni = ["Roma", "Parigi", "Tokyo", "New York", "Il Cairo"]

prezzi_destinazioni = {
    "Roma": 300,
    "Parigi": 450,
    "Tokyo": 1200,
    "New York": 1500,
    "Il Cairo": 800
}

# PARTE 2 – OOP

class Cliente:

    def __init__(self, nome, eta, vip):
        self.nome = nome
        self.eta = eta
        self.vip = vip

    def info(self):
        print(f"Cliente: {self.nome} | Età: {self.eta} | VIP: {self.vip}")


class Viaggio:

    def __init__(self, destinazione, prezzo, durata):
        self.destinazione = destinazione
        self.prezzo = prezzo
        self.durata = durata


class Prenotazione:

    def __init__(self, cliente, viaggio):
        self.cliente = cliente
        self.viaggio = viaggio

    def prezzo_finale(self):

        prezzo = self.viaggio.prezzo

        if self.cliente.vip:
            prezzo = prezzo * 0.9

        return prezzo

    def dettagli(self):

        print("Prenotazione:")
        print("Cliente:", self.cliente.nome)
        print("Destinazione:", self.viaggio.destinazione)
        print("Durata:", self.viaggio.durata, "giorni")
        print("Prezzo finale:", self.prezzo_finale())


# PARTE 3 – NumPy


prezzi_simulati = np.random.randint(200, 2000, 100)

media = np.mean(prezzi_simulati)
minimo = np.min(prezzi_simulati)
massimo = np.max(prezzi_simulati)
dev_std = np.std(prezzi_simulati)

percentuale_sopra_media = np.sum(prezzi_simulati > media) / len(prezzi_simulati) * 100

print("\nStatistiche prenotazioni simulate")
print("Prezzo medio:", media)
print("Prezzo minimo:", minimo)
print("Prezzo massimo:", massimo)
print("Deviazione standard:", dev_std)
print("Percentuale sopra la media:", percentuale_sopra_media)

# PARTE 4 – Pandas


clienti = ["Cliente_" + str(i) for i in range(1, 101)]
dest = np.random.choice(destinazioni, 100)
prezzi = np.random.randint(200, 2000, 100)
giorni = np.random.randint(1, 30, 100)
durate = np.random.randint(3, 15, 100)

df = pd.DataFrame({
    "Cliente": clienti,
    "Destinazione": dest,
    "Prezzo": prezzi,
    "Giorno_Partenza": giorni,
    "Durata": durate
})

df["Incasso"] = df["Prezzo"]

incasso_totale = df["Incasso"].sum()
incasso_medio_dest = df.groupby("Destinazione")["Incasso"].mean()
top_dest = df["Destinazione"].value_counts().head(3)

print("\nIncasso totale:", incasso_totale)
print("\nIncasso medio per destinazione:")
print(incasso_medio_dest)

print("\nTop 3 destinazioni più vendute:")
print(top_dest)

# PARTE 5 – Matplotlib


incasso_per_dest = df.groupby("Destinazione")["Incasso"].sum()

plt.figure()
incasso_per_dest.plot(kind="bar")
plt.title("Incasso per destinazione")
plt.ylabel("Incasso")
plt.show()

incasso_giornaliero = df.groupby("Giorno_Partenza")["Incasso"].sum()

plt.figure()
incasso_giornaliero.plot(kind="line")
plt.title("Andamento giornaliero incassi")
plt.ylabel("Incasso")
plt.show()

vendite_dest = df["Destinazione"].value_counts()

plt.figure()
vendite_dest.plot(kind="pie", autopct="%1.1f%%")
plt.title("Percentuale vendite per destinazione")
plt.ylabel("")
plt.show()

# PARTE 6 – Analisi Avanzata

categorie = {
    "Roma": "Europa",
    "Parigi": "Europa",
    "Tokyo": "Asia",
    "New York": "America",
    "Il Cairo": "Africa"
}

df["Categoria"] = df["Destinazione"].map(categorie)

incasso_categoria = df.groupby("Categoria")["Incasso"].sum()
durata_media_categoria = df.groupby("Categoria")["Durata"].mean()

print("\nIncasso per categoria:")
print(incasso_categoria)

print("\nDurata media per categoria:")
print(durata_media_categoria)

df.to_csv("prenotazioni_analizzate.csv", index=False)

# PARTE 7 – Estensioni

def top_clienti(df, n):

    conteggio = df["Cliente"].value_counts().head(n)
    return conteggio

print("\nTop clienti:")
print(top_clienti(df, 5))


# Grafico combinato

incasso_medio_categoria = df.groupby("Categoria")["Incasso"].mean()

fig, ax1 = plt.subplots()

ax1.bar(incasso_medio_categoria.index, incasso_medio_categoria.values)
ax1.set_ylabel("Incasso medio")

ax2 = ax1.twinx()
ax2.plot(durata_media_categoria.index, durata_media_categoria.values, marker="o")
ax2.set_ylabel("Durata media")

plt.title("Incasso medio e durata media per categoria")
plt.show()