import numpy as np

# Parte 1 – Variabili

# Paziente 1
nome1 = "Aldo"
cognome1 = "Baglio"
codice_fiscale1 = "BLG12345"
eta1 = 45
peso1 = 78.5
analisi1 = ["emocromo", "glicemia", "colesterolo"]

# Paziente 2
nome2 = "Giovanni"
cognome2 = "Storti"
codice_fiscale2 = "STR67890"
eta2 = 50
peso2 = 82.3
analisi2 = ["glicemia", "trigliceridi", "colesterolo"]

# Paziente 3
nome3 = "Giacomo"
cognome3 = "Poretti"
codice_fiscale3 = "PRT54321"
eta3 = 47
peso3 = 76.8
analisi3 = ["emocromo", "vitamina D", "glicemia"]


# Classe Paziente
class Paziente:

    def __init__(self, nome, cognome, codice_fiscale, eta, peso, analisi_effettuate, risultati_analisi):
        self.nome = nome
        self.cognome = cognome
        self.codice_fiscale = codice_fiscale
        self.eta = eta
        self.peso = peso
        self.analisi_effettuate = analisi_effettuate
        self.risultati_analisi = risultati_analisi

    def scheda_personale(self):
        return f"Paziente: {self.nome} {self.cognome} | CF: {self.codice_fiscale} | Età: {self.eta} | Peso: {self.peso} kg"

    def statistiche_analisi(self):
        media = np.mean(self.risultati_analisi)
        minimo = np.min(self.risultati_analisi)
        massimo = np.max(self.risultati_analisi)
        deviazione = np.std(self.risultati_analisi)

        print("Statistiche analisi:")
        print("Media:", media)
        print("Minimo:", minimo)
        print("Massimo:", massimo)
        print("Deviazione standard:", deviazione)


# Classe Medico

class Medico:

    def __init__(self, nome, cognome, specializzazione):
        self.nome = nome
        self.cognome = cognome
        self.specializzazione = specializzazione

    def visita_paziente(self, paziente):
        print(f"Il medico {self.nome} {self.cognome} ({self.specializzazione}) visita il paziente {paziente.nome} {paziente.cognome}")



# Classe Analisi

class Analisi:

    def __init__(self, tipo, risultato):
        self.tipo = tipo
        self.risultato = risultato

    def valuta(self):

        if self.tipo == "glicemia":
            if 70 <= self.risultato <= 110:
                return "Valore nella norma"
            else:
                return "Valore fuori norma"

        elif self.tipo == "colesterolo":
            if self.risultato < 200:
                return "Valore nella norma"
            else:
                return "Valore alto"

        else:
            return "Valore da valutare"


# Parte 3 – NumPy

valori_esame = np.array([90, 85, 100, 110, 95, 88, 92, 105, 98, 101])

print("Statistiche generali esame:")
print("Media:", np.mean(valori_esame))
print("Massimo:", np.max(valori_esame))
print("Minimo:", np.min(valori_esame))
print("Deviazione standard:", np.std(valori_esame))


# Parte 4 e 5 – Programma principale

if __name__ == "__main__":

    # Creazione medici
    medico1 = Medico("Mario", "Risi", "Cardiologia")
    medico2 = Medico("Luigi", "Mario", "Endocrinologia")
    medico3 = Medico("Anna", "Pepe", "Medicina generale")

    # Creazione pazienti
    p1 = Paziente("Aldo", "Baglio", "BLG123", 45, 78.5,
                  ["emocromo", "glicemia", "colesterolo"],
                  np.array([90, 180, 13]))

    p2 = Paziente("Giovanni", "Storti", "STR456", 50, 82.3,
                  ["glicemia", "trigliceridi", "colesterolo"],
                  np.array([105, 210, 190]))

    p3 = Paziente("Giacomo", "Poretti", "PRT789", 47, 76.8,
                  ["emocromo", "vitamina D", "glicemia"],
                  np.array([14, 35, 95]))

    p4 = Paziente("Laura", "Petrarca", "NRE321", 39, 60.4,
                  ["glicemia", "colesterolo", "emocromo"],
                  np.array([99, 170, 12]))

    p5 = Paziente("Marco", "Boccaccio", "BLU654", 55, 85.2,
                  ["trigliceridi", "glicemia", "colesterolo"],
                  np.array([220, 115, 205]))

    pazienti = [p1, p2, p3, p4, p5]

    print("\n--- SCHEDE PAZIENTI ---")

    for p in pazienti:
        print(p.scheda_personale())
        p.statistiche_analisi()
        print()

    print("\n--- VISITE MEDICHE ---")

    medico1.visita_paziente(p1)
    medico2.visita_paziente(p2)
    medico3.visita_paziente(p3)
    medico1.visita_paziente(p4)
    medico2.visita_paziente(p5)