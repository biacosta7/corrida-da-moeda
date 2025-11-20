import matplotlib.pyplot as plt

class Grafico:
    def __init__(self):
        self.frequencias = []  # lista de P(cara) a cada lançamento
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Distribuição Empírica da Moeda")
        self.ax.set_xlabel("Número de lançamentos")
        self.ax.set_ylabel("Probabilidade de Cara")

    def atualizar(self):
        from eventos import sim  # evita import circular

        if sim.total == 0:
            return

        # probabilidade empírica
        p_cara = sim.cara / sim.total
        self.frequencias.append(p_cara)

        # redesenhar
        self.ax.clear()
        self.ax.plot(self.frequencias, label="P(cara) empírica")

        # linha teórica
        self.ax.axhline(0.5, color='red', linestyle='--', label="P(cara) teórica = 0.5")

        self.ax.set_title("Distribuição Empírica da Moeda")
        self.ax.set_xlabel("Número de lançamentos")
        self.ax.set_ylabel("Probabilidade de Cara")
        self.ax.set_ylim(0, 1)

        self.ax.legend()
        plt.pause(0.001)
