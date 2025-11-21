# main.py

import pygame
import sys
from assets import *
from corrida import GameManager
from interface import BoardDrawer
from plots.grafico import Grafico # Importa o gráfico de probabilidade

def main():
    # Inicialização do Pygame
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Corrida da Moeda e Distribuição Binomial")
    
    # Inicialização do Jogo e Gráfico
    game_manager = GameManager()
    board_drawer = BoardDrawer(screen, game_manager)
    
    # Inicializa o gráfico (janela separada)
    grafico = Grafico()

    # Loop principal do jogo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Lançar moeda ao clicar com o mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_manager.jogo_ativo:
                    game_manager.executar_turno()
                    grafico.atualizar() # Atualiza o gráfico a cada lançamento

        # Desenho da tela
        screen.fill(COR_PRETO) # Fundo preto
        board_drawer.desenhar_tudo()
        
        # Status do Jogo
        font_status = pygame.font.Font(None, 30)
        
        if game_manager.jogo_ativo:
            texto_turno = f"Turno: Jogador {game_manager.jogador_atual_idx + 1}"
            texto_status = font_status.render(texto_turno, True, COR_BRANCO)
        else:
            texto_vitoria = f"Vencedor: Jogador {game_manager.vencedor.id + 1}!"
            texto_status = font_status.render(texto_vitoria, True, COR_BRANCO)
            
        screen.blit(texto_status, (10, 10))


        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # É necessário ter os assets de imagem na pasta de execução, ex:
    # porco-amarelo.png, porco-rosa.png, etc.
    main()