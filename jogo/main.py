# main.py (Código completo com a lógica de delay)

import math
import pygame
import sys
from assets import *
from corrida import GameManager
from interface import BoardDrawer
from plots.grafico import Grafico 

DELAY_PASSAR_TURNO_MS = 1000 # 1000 milissegundos = 1 segundo
tempo_lancamento = 0
lancamento_completo = False # Indica que a moeda foi clicada e o resultado está sendo exibido

def verificar_clique_moeda(mouse_pos, drawer, grafico):
    """Verifica se o clique foi no botão da moeda, lança e retorna o tempo de início do delay."""
    
    global lancamento_completo # Precisamos acessar o estado global
    
    game_manager = drawer.game
    
    if not game_manager.jogo_ativo or lancamento_completo:
        # Ignora cliques se o jogo não está ativo ou se o resultado já está sendo exibido
        return False, 0
        
    jogador_ativo_idx = game_manager.jogador_atual_idx
    cx, cy = drawer.coordenadas_moeda_botao[jogador_ativo_idx]
    raio = 20
    
    distancia = math.hypot(mouse_pos[0] - cx, mouse_pos[1] - cy)
    
    if distancia <= raio:
        # 1. Lançar a moeda e obter o resultado (C ou K)
        resultado = game_manager.lancar_moeda()
        
        # 2. Atualizar o estado da interface (para o desenho)
        drawer.resultado_texto = resultado
        
        # 3. Processar movimento e depósito (MAS NÃO PASSA O TURNO)
        game_manager.processar_movimento_e_deposito(resultado) # ✅ NOME DO MÉTODO ATUALIZADO
        
        # 4. Atualiza o gráfico 
        grafico.atualizar()
        
        # 5. Configura o estado de delay
        lancamento_completo = True # Bloqueia novos cliques
        return True, pygame.time.get_ticks() # Retorna o tempo atual
        
    return False, 0

def main():
    global tempo_lancamento, lancamento_completo # Usa as variáveis de estado
    
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Corrida da Moeda e Distribuição Binomial")
    
    game_manager = GameManager()
    board_drawer = BoardDrawer(screen, game_manager)
    grafico = Grafico()

    running = True
    while running:
        
        tempo_atual = pygame.time.get_ticks() # Pega o tempo atual do Pygame
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Lidar com o clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicou, tempo_inicio = verificar_clique_moeda(event.pos, board_drawer, grafico)
                if clicou:
                    tempo_lancamento = tempo_inicio
        
        if lancamento_completo:
            if (tempo_atual - tempo_lancamento) >= DELAY_PASSAR_TURNO_MS:
                
                # 1. Passa o turno
                game_manager.proximo_jogador()
                
                # 2. Limpa o resultado na interface (para que ele não apareça no novo jogador)
                board_drawer.resultado_texto = "" 
                
                # 3. Reseta o estado
                lancamento_completo = False 

        # Desenho da tela
        screen.fill(COR_PRETO) 
        board_drawer.desenhar_tudo()
        
        # Status do Jogo
        font_status = pygame.font.Font(None, 30)
        
        if game_manager.jogo_ativo:
            # Mostra o jogador atual, mesmo durante o delay
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
    main()