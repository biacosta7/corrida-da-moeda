# interface.py

import pygame
import math
from assets import *
from corrida import GameManager

class BoardDrawer:
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game = game_manager
        
        # Carregar e redimensionar assets
        self.assets_carregados = {}
        for nome, caminho in ASSETS.items():
            try:
                img = pygame.image.load(caminho).convert_alpha()
                # Redimensionar porquinhos e o saco
                if 'porco' in nome:
                    self.assets_carregados[nome] = pygame.transform.scale(img, (70, 70))
                elif nome == 'bag':
                    self.assets_carregados[nome] = pygame.transform.scale(img, (100, 100))
            except pygame.error:
                print(f"Erro ao carregar imagem: {caminho}. Usando um placeholder.")
                self.assets_carregados[nome] = pygame.Surface((70, 70))
                self.assets_carregados[nome].fill(COR_PRETO) # Placeholder

        self.font = pygame.font.Font(None, 24)
        self.tamanho_bloco = TAMANHO_BLOCO
        self.caminho_tamanho = CAMINHO_TAMANHO

        # Definir as coordenadas dos cantos para cada jogador
        self.coordenadas_canto = {
            0: (50, 50), # Amarelo (Superior Esquerdo)
            1: (LARGURA_TELA - 120, 50), # Roxo (Superior Direito)
            2: (50, ALTURA_TELA - 120), # Rosa (Inferior Esquerdo)
            3: (LARGURA_TELA - 120, ALTURA_TELA - 120), # Azul (Inferior Direito)
        }
        
        # Coordenadas do centro
        self.centro_x = LARGURA_TELA // 2
        self.centro_y = ALTURA_TELA // 2
        
    def _desenhar_moedas(self, screen, x, y, cor_fundo, num_moedas):
        """Desenha as moedas (círculos '3') sobre a imagem do porquinho."""
        
        # Coordenadas relativas para o texto '3'
        posicoes = [(-20, -20), (0, -20), (20, -20), 
                    (-20, 0), (0, 0), (20, 0)]
        
        # Garante que só desenhe até o número total de moedas por porco
        moedas_a_desenhar = min(num_moedas, 6) 
        
        for i in range(moedas_a_desenhar):
            moeda_x = x + posicoes[i][0] + 35 # 35 = metade da largura do porco
            moeda_y = y + posicoes[i][1] + 35
            
            # Desenha um pequeno círculo com a cor de fundo (para o '3')
            pygame.draw.circle(screen, cor_fundo, (moeda_x, moeda_y), 10)
            
            # Desenha o número '3'
            texto = self.font.render("3", True, COR_BRANCO)
            screen.blit(texto, (moeda_x - 5, moeda_y - 8))
            
    def _desenhar_porquinhos(self):
        """Desenha os 4 porquinhos e suas moedas."""
        
        # Mapeamento do jogador para o asset de imagem
        asset_map = {0: "amarelo", 1: "roxo", 2: "rosa", 3: "azul"}
        
        for i, jogador in enumerate(self.game.jogadores):
            x_canto, y_canto = self.coordenadas_canto[i]
            
            # Desenha o bloco de cor do porquinho (Fundo)
            pygame.draw.rect(self.screen, jogador.cor, (x_canto, y_canto, 100, 100), 0, 5)

            # Desenha a imagem do porquinho 
            self.assets_carregados = {}
            for nome, caminho in ASSETS.items():
                try:
                    img = pygame.image.load(caminho).convert_alpha()
                    # Redimensionar porquinhos e o saco
                    if 'porco' in nome:
                        self.assets_carregados[nome] = pygame.transform.scale(img, (70, 70))
                    elif nome == 'bag':
                        self.assets_carregados[nome] = pygame.transform.scale(img, (100, 100))
                except pygame.error:
                    print(f"Erro ao carregar imagem: {caminho}. Usando um placeholder.")
                    # 2. Use o placeholder genérico em caso de falha de carregamento
                    if 'porco' in nome:
                        self.assets_carregados[nome] = self.placeholder_porco
                    elif nome == 'bag':
                        self.assets_carregados[nome] = pygame.transform.scale(self.placeholder_porco, (100, 100))


    def _desenhar_caminho(self):
        """Desenha os caminhos de blocos para o centro."""
        
        offsets = { # Offsets para desenhar os caminhos em relação ao centro
            0: (0, -1),   # Amarelo (Superior)
            1: (1, 0),    # Roxo (Direito)
            2: (0, 1),    # Rosa (Inferior)
            3: (-1, 0),   # Azul (Esquerdo)
        }
        
        for i, cor in enumerate(self.game.cores_tabuleiro):
            dx, dy = offsets[i]
            
            for j in range(1, self.caminho_tamanho + 1):
                # Posição do bloco
                bloco_x = self.centro_x + dx * self.tamanho_bloco * (j + 1)
                bloco_y = self.centro_y + dy * self.tamanho_bloco * (j + 1)
                
                # Desenha o quadrado
                pygame.draw.rect(self.screen, cor, 
                                 (bloco_x - self.tamanho_bloco // 2, 
                                  bloco_y - self.tamanho_bloco // 2, 
                                  self.tamanho_bloco, self.tamanho_bloco))
                                  
    def _desenhar_centro(self):
        """Desenha o círculo central e o saco de moedas."""
        
        # Círculo Branco Central
        pygame.draw.circle(self.screen, COR_BRANCO, (self.centro_x, self.centro_y), 70)
        
        # Saco de Moedas (BAG)
        bag_img = self.assets_carregados.get('bag', pygame.Surface((100, 100))) 
        self.screen.blit(bag_img, (self.centro_x - 50, self.centro_y - 50))
        
        # Desenhar os contadores (0 de cada jogador)
        raio_contador = 40
        font_grande = pygame.font.Font(None, 36)
        
        for i, jogador in enumerate(self.game.jogadores):
            # Posições relativas ao centro
            pos_relativa = {
                0: (-raio_contador, -raio_contador), # Amarelo (Cima-Esquerda)
                1: (raio_contador, -raio_contador),  # Roxo (Cima-Direita)
                2: (-raio_contador, raio_contador),  # Rosa (Baixo-Esquerda)
                3: (raio_contador, raio_contador),   # Azul (Baixo-Direita)
            }
            
            offset_x, offset_y = pos_relativa[i]
            contador_x = self.centro_x + offset_x
            contador_y = self.centro_y + offset_y

            # Desenha o contador
            texto = font_grande.render(str(jogador.moedas_depositadas), True, jogador.cor)
            self.screen.blit(texto, (contador_x - texto.get_width() // 2, 
                                     contador_y - texto.get_height() // 2))

    def _desenhar_indicadores(self):
        """Desenha as bolinhas que representam os jogadores nos caminhos."""
        
        offsets = { 
            0: (0, -1),   # Amarelo
            1: (1, 0),    # Roxo
            2: (0, 1),    # Rosa
            3: (-1, 0),   # Azul
        }
        
        for i, jogador in enumerate(self.game.jogadores):
            if jogador.posicao_caminho > 0:
                dx, dy = offsets[i]
                j = jogador.posicao_caminho 
                
                # A posição 5 é o centro, 4 é o bloco antes.
                # A bolinha fica sobre o bloco (j), a posição 0 é o início (fora do caminho).
                
                bloco_x = self.centro_x + dx * self.tamanho_bloco * (self.caminho_tamanho + 1 - j)
                bloco_y = self.centro_y + dy * self.tamanho_bloco * (self.caminho_tamanho + 1 - j)
                
                # Desenha a bolinha (indicador)
                pygame.draw.circle(self.screen, jogador.cor, (bloco_x, bloco_y), self.tamanho_bloco // 3)
                
    def desenhar_tudo(self):
        """Desenha todos os elementos do jogo."""
        self._desenhar_caminho()
        self._desenhar_porquinhos()
        self._desenhar_centro()
        self._desenhar_indicadores()