import math
import pygame
import sys

# novo config
from config_assets import *  

from corrida import GameManager
from interface import BoardDrawer
from plots.grafico import Grafico


DELAY_PASSAR_TURNO_MS = 1000
tempo_lancamento = 0
lancamento_completo = False


def verificar_clique_moeda(mouse_pos, drawer, grafico):
    global lancamento_completo

    game_manager = drawer.game

    if not game_manager.jogo_ativo or lancamento_completo:
        return False, 0

    jogador_ativo_idx = game_manager.jogador_atual_idx
    cx, cy = drawer.coordenadas_moeda_botao[jogador_ativo_idx]
    raio = drawer.RAIO_MOEDA_BOTAO

    distancia = math.hypot(mouse_pos[0] - cx, mouse_pos[1] - cy)

    if distancia <= raio:
        # 1. Lança moeda
        resultado = game_manager.lancar_moeda()

        # 2. Atualiza interface e gráfico
        drawer.resultado_texto = resultado
        
        # 3. Atualiza movimento no tabuleiro
        game_manager.processar_movimento_e_deposito(resultado)

        # 4. Marca delay
        lancamento_completo = True
        return True, pygame.time.get_ticks()

    return False, 0


def main():
    global tempo_lancamento, lancamento_completo

    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Corrida da Moeda e Distribuição Binomial")

    # Gerente do jogo
    game_manager = GameManager()

    # Interface gráfica
    board_drawer = BoardDrawer(screen, game_manager)

    # Gráfico — agora precisa receber a simulação
    grafico = Grafico(game_manager.simulacao)

    primeiro_lancamento = False

    running = True
    while running:
        tempo_atual = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicou, tempo_inicio = verificar_clique_moeda(event.pos, board_drawer, grafico)
                if clicou:
                    tempo_lancamento = tempo_inicio
                    primeiro_lancamento = True

        # Delay do próximo turno
        if lancamento_completo:
            if tempo_atual - tempo_lancamento >= DELAY_PASSAR_TURNO_MS:
                game_manager.proximo_jogador()
                board_drawer.resultado_texto = ""
                lancamento_completo = False

        screen.fill(COR_PRETO)
        board_drawer.desenhar_tudo()

        # GRÁFICO: Agora a chamada retorna ao loop principal
        # Mas só atualizamos/desenhamos se houver dados (após o primeiro clique)
        if game_manager.simulacao.total > 0: # Verifica se há lançamentos registrados
             # Usamos a nova posição que você definiu
             grafico.atualizar(screen, pos=(750, 40))

        # Status do jogo
        font_status = pygame.font.Font(None, 30)

        if game_manager.jogo_ativo:
            texto_turno = f"Turno: Jogador {game_manager.jogador_atual_idx + 1}"
            texto_status = font_status.render(texto_turno, True, COR_BRANCO)
        else:
            texto_vitoria = f"Vencedor: Jogador {game_manager.vencedor.id + 1}!"
            texto_status = font_status.render(texto_vitoria, True, COR_BRANCO)

        screen.blit(texto_status, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
