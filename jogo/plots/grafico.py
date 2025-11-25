import matplotlib
matplotlib.use("Agg")   # backend sem janela

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pygame
import numpy as np


class Grafico:
    def __init__(self, simulacao):
        self.simulacao = simulacao
        self.frequencias = []
        self.fig = None
        self.ax = None
        self.canvas = None

    def _init_canvas(self):
        if self.fig is None:
            self.fig, self.ax = plt.subplots(figsize=(3, 2))
            self.canvas = FigureCanvasAgg(self.fig)
            

    def atualizar(self, superficie_destino, pos=(720, 20)):
        """Desenha o gráfico na tela do pygame."""
        self._init_canvas()

        self.total = self.simulacao.total
        self.cara = self.simulacao.cara

        if self.total == 0:
            return

        prob = self.cara / self.total
        self.frequencias.append(prob)

        self.ax.clear()
        self.ax.plot(self.frequencias)
        self.ax.axhline(0.5, linestyle="--")

        self.fig.tight_layout()
        self.canvas.draw()

        # CORREÇÃO: Trocar tostring_rgb() por tostring_argb()
        buf = np.frombuffer(self.canvas.tostring_argb(), dtype=np.uint8)
        w, h = self.fig.canvas.get_width_height()
        # Não é necessário mudar o reshape se você usar ARGB/RGB, mas o buffer tem 4 canais agora (RGBA)
        # O Pygame pode lidar com o buffer ARGB e o formato 'ARGB'
        buf = buf.reshape(h, w, 4) # 4 canais (A, R, G, B)

        # CORREÇÃO: Trocar o formato de cor de saída para "ARGB"
        surf = pygame.image.frombuffer(buf.tobytes(), (w, h), "ARGB") 
        superficie_destino.blit(surf, pos)
