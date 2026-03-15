# Variabili 

titolo = "L'esperto compratore di gemme"   
copie = 6                                  
prezzo_medio = 21.40                       
disponibile = True                         

print("Titolo:", titolo)
print("Copie disponibili:", copie)
print("Prezzo medio:", prezzo_medio)
print("Disponibile:", disponibile)

# Lista di libri
lista_libri = [
    "Il mondo invisibile",
    "La paranza dei bambini",
    "Critica del giudizio",
    "Istruzioni per vivere in pace",
    "One piece"
]

print("\nLista libri:", lista_libri)


# Dizionario titolo -> copie
copie_libri = {
    "Il mondo invisibile": 6,
    "La paranza dei bambini": 1,
    "Critica del giudizio": 7,
    "Istruzioni per vivere in pace": 3,
    "One piece": 2
}

print("\nCopie per libro:", copie_libri)


# Utenti registrati
utenti_registrati = ["Aldo", "Mauro", "Luca", "Eloisa"] 

print("\nUtenti registrati:", utenti_registrati)


class Libro:

    def __init__(self, titolo, autore, anno, copie_disponibili):
        self.titolo = titolo
        self.autore = autore
        self.anno = anno
        self.copie_disponibili = copie_disponibili

    def info(self):
        return f"{self.titolo} di {self.autore} ({self.anno}) - Copie disponibili: {self.copie_disponibili}"


class Utente:

    def __init__(self, nome, eta, id_utente):
        self.nome = nome
        self.eta = eta
        self.id_utente = id_utente

    def scheda(self):
        print(f"Utente: {self.nome} | Età: {self.eta} | ID: {self.id_utente}")


class Prestito:

    def __init__(self, utente, libro, giorni):
        self.utente = utente
        self.libro = libro
        self.giorni = giorni

    def dettagli(self):
        print(f"Prestito: {self.utente.nome} ha preso '{self.libro.titolo}' per {self.giorni} giorni")


# Funzione per prestare un libro
def presta_libro(utente, libro, giorni):

    if libro.copie_disponibili > 0:
        libro.copie_disponibili -= 1
        prestito = Prestito(utente, libro, giorni)
        return prestito
    else:
        print(f"Il libro '{libro.titolo}' non è disponibile.")
        return None


if __name__ == "__main__":

    # Creazione libri
    libro1 = Libro("Il mondo invisibile", "Ignoto", 1932, 6)
    libro2 = Libro("Il nome della rosa", "Umberto Eco", 1980, 1)
    libro3 = Libro("Critica del giudizio", "Immanuel Kant", 1790, 7)

    # Creazione utenti
    utente1 = Utente("Aldo", 21, 101)
    utente2 = Utente("Mauro", 22, 102)
    utente3 = Utente("Luca", 30, 103)

    # Simulazione prestiti
    prestiti = []

    p1 = presta_libro(utente1, libro1, 7)
    p2 = presta_libro(utente2, libro2, 10)
    p3 = presta_libro(utente3, libro3, 5)

    if p1:
        prestiti.append(p1)
    if p2:
        prestiti.append(p2)
    if p3:
        prestiti.append(p3)

    # Stampa dettagli prestiti
    print("\n--- Prestiti effettuati ---")

    for prestito in prestiti:
        prestito.dettagli()