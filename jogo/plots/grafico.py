import matplotlib
matplotlib.use("Agg")   # backend sem janela

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pygame
import numpy as np


class Grafico:
    def __init__(self):
        self.cara = 0
        self.total = 0
        self.frequencias = []
        self.fig = None
        self.ax = None
        self.canvas = None

    def registrar_lancamento(self, resultado):
        """Registra o lançamento da moeda vinda do GameManager."""
        self.total += 1
        if resultado == "C":  # o jogo usa C/K
            self.cara += 1

    def _init_canvas(self):
        if self.fig is None:
            self.fig, self.ax = plt.subplots(figsize=(3, 2))
            self.canvas = FigureCanvasAgg(self.fig)

    def atualizar(self, superficie_destino, pos=(720, 20)):
        """Desenha o gráfico na tela do pygame."""
        self._init_canvas()

        if self.total == 0:
            return

        prob = self.cara / self.total
        self.frequencias.append(prob)

        self.ax.clear()
        self.ax.plot(self.frequencias)
        self.ax.axhline(0.5, linestyle="--")

        self.fig.tight_layout()
        self.canvas.draw()

        buf = np.frombuffer(self.canvas.tostring_rgb(), dtype=np.uint8)
        w, h = self.fig.canvas.get_width_height()
        buf = buf.reshape(h, w, 3)

        surf = pygame.image.frombuffer(buf.tobytes(), (w, h), "RGB")
        superficie_destino.blit(surf, pos)
