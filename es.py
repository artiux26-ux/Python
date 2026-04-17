class Student:
    def __init__(self,nome, eta, corso):
        self.nome = nome
        self.eta = eta
        self.corso = corso
    @classmethod
    def stringa_tipo(cls, stringa):
        nome, eta, corso = stringa.split("-")
        return cls(nome, int(eta), corso)

    @property
    def anno_di_nascita(self):
        return 2028 - self.eta
    @property
    def eta(self):
        return self._eta
    @eta.setter
    def eta(self, value):
        if value < 0:
            print("L'età non può essere negativa")
            self._eta = 0
        else:          
             self._eta = value

s = Student.stringa_tipo("Aldo-25-Matematica")
print(s.nome, s.eta, s.corso)
print("Il tuo anno di nascita è:",s.anno_di_nascita)
