import matplotlib.pyplot as plt
from plots.teorica import calcular_teorica

class Grafico:
    def __init__(self):
        self.resultados = []
        plt.ion()
        self.fig, self.ax = plt.subplots()

    def atualizar(self, r):
        self.resultados.append(1 if r == "H" else 0)
        self.ax.clear()

        # Histograma empírico
        self.ax.hist(self.resultados, bins=[-0.5,0.5,1.5], rwidth=0.8, color='gray', label="Empírico")

        # Distribuição teórica
        teorica = calcular_teorica(len(self.resultados))
        self.ax.plot([0,1], teorica, color='red', marker='o', label="Teórico")

        self.ax.set_xticks([0, 1])
        self.ax.set_xticklabels(["Coroa", "Cara"])
        self.ax.set_ylim(0, 1)

        self.ax.legend()
        plt.pause(0.001)
