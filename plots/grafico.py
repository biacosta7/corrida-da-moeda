import matplotlib.pyplot as plt
from plots.teorica import calcular_teorica

class Grafico:
    def __init__(self):
        self.resultados = []
        plt.ion()
        self.fig, self.ax = plt.subplots()

    def atualizar(self, rA, rB):
        self.resultados.append(rA)
        self.ax.clear()
        self.ax.hist(self.resultados, bins=[-0.5,0.5,1.5], rwidth=0.8, color='gray')
        
        teorica = calcular_teorica(len(self.resultados))
        self.ax.plot(teorica, color='red')

        plt.pause(0.001)
