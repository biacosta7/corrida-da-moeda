import pygame
from corrida import Personagem
from eventos import lancar_moeda

class GameInterface:
    def __init__(self, grafico):
        pygame.init()
        self.tela = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Corrida da Moeda")
        self.clock = pygame.time.Clock()
        self.grafico = grafico

        self.A = Personagem("A")
        self.B = Personagem("B")

        self.fonte = pygame.font.SysFont("Arial", 24)

    def desenhar_personagens(self):
        pygame.draw.circle(self.tela, (0, 150, 255), (100 + self.A.x, 200), 25)
        pygame.draw.circle(self.tela, (255, 120, 0), (100 + self.B.x, 400), 25)

        textoA = self.fonte.render(f"A: {self.A.pontuacao}", True, (255,255,255))
        textoB = self.fonte.render(f"B: {self.B.pontuacao}", True, (255,255,255))

        self.tela.blit(textoA, (50, 150))
        self.tela.blit(textoB, (50, 350))

    def atualizar(self):
        resultado = lancar_moeda()

        if resultado == "H":
            self.A.avancar()
        else:
            self.B.avancar()

        return resultado

    def loop(self):
        rodando = True

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

            r = self.atualizar()
            self.grafico.atualizar(r)

            self.tela.fill((30, 30, 30))
            self.desenhar_personagens()

            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()
