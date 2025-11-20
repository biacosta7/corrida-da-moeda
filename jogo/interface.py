# interface.py

import pygame
import math
import os # ESSENCIAL: Para construção robusta de caminhos de arquivo
from assets import *
from corrida import GameManager

# Determina o diretório absoluto onde este script (interface.py) está
# Isso garante que a busca por assets comece na pasta 'jogo/'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class BoardDrawer:
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game = game_manager
        
        # Placeholder genérico (usado em caso de falha de carregamento)
        self.placeholder_porco = pygame.Surface((70, 70))
        self.placeholder_porco.fill((100, 100, 100)) # Cor cinza para visualização
        
        # Carregar e redimensionar assets
        self.assets_carregados = {}
        for nome, nome_arquivo in ASSETS.items():
            
            # CONSTRUÇÃO DO CAMINHO CORRIGIDA: Junta o diretório do script (jogo/) 
            # com o caminho relativo do asset (ex: assets/porco-amarelo.png)
            caminho_completo = os.path.join(SCRIPT_DIR, nome_arquivo) 
            
            try:
                # Tenta carregar usando o caminho absoluto
                img = pygame.image.load(caminho_completo).convert_alpha()
                
                # Redimensionar porquinhos e o saco
                if 'porco' in nome:
                    self.assets_carregados[nome] = pygame.transform.scale(img, (70, 70))
                elif nome == 'bag':
                    self.assets_carregados[nome] = pygame.transform.scale(img, (100, 100))
            except pygame.error as e:
                # Se falhar (FileNotFoundError ou outro erro Pygame), usa o placeholder
                print(f"Erro ao carregar imagem: {nome_arquivo} em {caminho_completo}. Usando placeholder. Erro: {e}")
                
                if 'porco' in nome:
                    self.assets_carregados[nome] = self.placeholder_porco
                elif nome == 'bag':
                    # O placeholder para a bolsa precisa ser redimensionado
                    self.assets_carregados[nome] = pygame.transform.scale(self.placeholder_porco, (100, 100))


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
        # Assumindo que 6 é o número máximo de moedas visíveis no canto (3 moedas * 2 slots por porco)
        moedas_a_desenhar = min(num_moedas, TOTAL_MOEDAS_INICIAIS) 
        
        for i in range(moedas_a_desenhar):
            moeda_x = x + posicoes[i][0] + 35 # 35 = metade da largura do porco
            moeda_y = y + posicoes[i][1] + 35
            
            # Desenha um pequeno círculo com a cor de fundo (para o '3')
            pygame.draw.circle(screen, cor_fundo, (moeda_x, moeda_y), 10)
            
            # Desenha o número '3' (A moeda representa 3 moedas de um porquinho)
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
            asset_nome = asset_map[i]
            # Usa .get() com o placeholder seguro como valor padrão
            porquinho_img = self.assets_carregados.get(asset_nome, self.placeholder_porco) 
            
            # Posições dos 4 porquinhos (simplificação, 2x2)
            # O design da imagem sugere 4 porquinhos por canto, um para cada moeda inicial (3 moedas/porco * 4 porcos = 12 moedas)
            pos_porcos = [
                (x_canto + 5, y_canto + 5), (x_canto + 50, y_canto + 5),
                (x_canto + 5, y_canto + 50), (x_canto + 50, y_canto + 50)
            ]
            
            # Total de moedas iniciais: 12. Cada jogador começa com 4 "porquinhos-moeda"
            num_porquinhos_visiveis = math.ceil(jogador.moedas_no_porco / MOEDAS_INICIAIS_POR_PORCO)
            
            for j in range(NUM_PORCOS):
                 # Desenha o porquinho se ele ainda tiver moedas associadas (simplificação visual)
                if j < num_porquinhos_visiveis:
                    self.screen.blit(porquinho_img, pos_porcos[j])
                else:
                    # Desenha um bloco vazio se o porquinho já depositou suas 3 moedas
                    pygame.draw.rect(self.screen, COR_PRETO, (pos_porcos[j][0], pos_porcos[j][1], 40, 40)) 


            # Desenha as moedas restantes no porco principal
            # NOTA: O indicador de moedas deve mostrar quantas "moedas de 3" ainda restam
            moedas_a_mostrar = num_porquinhos_visiveis
            self._desenhar_moedas(self.screen, x_canto, y_canto, jogador.cor, moedas_a_mostrar)


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
        
        # Saco de Moedas (BAG) - Usa o placeholder seguro como fallback
        bag_img_placeholder = pygame.transform.scale(self.placeholder_porco, (100, 100))
        bag_img = self.assets_carregados.get('bag', bag_img_placeholder) 
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
            # Desenha o indicador apenas se ele não estiver no início (posicao_caminho = 0)
            if jogador.posicao_caminho > 0:
                dx, dy = offsets[i]
                j = jogador.posicao_caminho 
                
                # Calcula a posição do bloco. A posição mais próxima do centro (j=1)
                # fica no bloco (caminho_tamanho + 1 - j)
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