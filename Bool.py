# Esercizio patente
utente= int(input("Quanti anni hai?: "))
patente= str(input("hai la patente?: "))
puo_guidare= (utente>=18) and (patente.startswith("si"))
print(puo_guidare)

# Biblioteca

impiegato= input("Sei in ritardo con la consegna (si/no)? : ")
impiegato_chiede= input("hai premium?: ")

in_ritardo= (impiegato == "si")
premium= ( impiegato_chiede == "si")
puo_entrare = (not in_ritardo) or premium
print(puo_entrare)