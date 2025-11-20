import pygame
from jogo.corrida import Personagem
from jogo.eventos import lancar_moeda

class GameInterface:
    def __init__(self, grafico):
        pygame.init()
        self.tela = pygame.display.set_mode((1200, 600))
        self.clock = pygame.time.Clock()
        self.grafico = grafico

        # Personagens
        self.A = Personagem("A", None)
        self.B = Personagem("B", None)

    def loop(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

            # Lançar moedas
            rA = lancar_moeda()
            rB = lancar_moeda()

            if rA == 1: self.A.avancar()
            if rB == 1: self.B.avancar()

            # Atualizar gráfico
            self.grafico.atualizar(rA, rB)

            # Renderizar corrida
            self.render()

            pygame.display.update()
            self.clock.tick(30)

    def render(self):
        self.tela.fill((30, 30, 30))
        pygame.draw.circle(self.tela, (0,255,0), (self.A.x + 50, 200), 20)
        pygame.draw.circle(self.tela, (0,0,255), (self.B.x + 50, 400), 20)
