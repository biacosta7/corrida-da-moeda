import random

class SimulacaoMoeda:
    def __init__(self):
        self.cara = 0
        self.coroa = 0
        self.total = 0

    def lancar(self):
        resultado = random.choice(["H", "T"])
        self.total += 1

        if resultado == "H":
            self.cara += 1
        else:
            self.coroa += 1

        return resultado

    def get_frequencias(self):
        if self.total == 0:
            return 0.5, 0.5
        return self.cara / self.total, self.coroa / self.total
