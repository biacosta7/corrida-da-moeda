# interface.py

import pygame
import math
import os 
from assets import * # Assumindo CAMINHO_TAMANHO = 9
from corrida import GameManager

# Determina o diretório absoluto onde este script (interface.py) está
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class BoardDrawer:
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game = game_manager
        
        # Placeholder genérico (usado em caso de falha de carregamento)
        self.placeholder_porco = pygame.Surface((70, 70))
        self.placeholder_porco.fill((100, 100, 100)) 
        
        # Carregar e redimensionar assets
        self.assets_carregados = {}
        for nome, nome_arquivo in ASSETS.items():
            
            # CONSTRUÇÃO DO CAMINHO: Junta o diretório do script (jogo/) 
            # com o caminho relativo do asset (ex: assets/porco-amarelo.png)
            caminho_completo = os.path.join(SCRIPT_DIR, nome_arquivo) 
            
            try:
                img = pygame.image.load(caminho_completo).convert_alpha()
                
                # Redimensionar porquinhos e o saco
                if 'porco' in nome:
                    self.assets_carregados[nome] = pygame.transform.scale(img, (70, 70))
                elif nome == 'bag':
                    self.assets_carregados[nome] = pygame.transform.scale(img, (100, 100))
            except pygame.error as e:
                print(f"Erro ao carregar imagem: {nome_arquivo} em {caminho_completo}. Usando placeholder. Erro: {e}")
                
                if 'porco' in nome:
                    self.assets_carregados[nome] = self.placeholder_porco
                elif nome == 'bag':
                    self.assets_carregados[nome] = pygame.transform.scale(self.placeholder_porco, (100, 100))


        self.font = pygame.font.Font(None, 24)
        self.tamanho_bloco = TAMANHO_BLOCO
        self.unidade_passo = UNIDADE_PASSO # NOVO
        self.caminho_tamanho = CAMINHO_TAMANHO # Deve ser 9

        # Definir as coordenadas dos cantos para cada jogador (Caixa 100x100)
        self.coordenadas_canto = {
            0: (50, 50), # Amarelo (Superior Esquerdo)
            1: (LARGURA_TELA - 120, 50), # Roxo (Superior Direito)
            2: (50, ALTURA_TELA - 120), # Rosa (Inferior Esquerdo)
            3: (LARGURA_TELA - 120, ALTURA_TELA - 120), # Azul (Inferior Direito)
        }
        
        # Coordenadas do centro
        self.centro_x = LARGURA_TELA // 2
        self.centro_y = ALTURA_TELA // 2
        
        # --- NOVO: Estrutura do Caminho (9 movimentos) ---
        self.path_movements = {
            # 0: Amarelo (7 Direita (+X), 2 Baixo (+Y))
            0: [(1, 0)] * 7 + [(0, 1)] * 2,
            # 1: Roxo (4 Baixo (+Y), 5 Esquerda (-X))
            1: [(0, 1)] * 4 + [(-1, 0)] * 5,
            # 2: Rosa (4 Cima (-Y), 5 Direita (+X))
            2: [(0, -1)] * 4 + [(1, 0)] * 5,
            # 3: Azul (7 Esquerda (-X), 2 Cima (-Y))
            3: [(-1, 0)] * 7 + [(0, -1)] * 2,
        }
        
        # Definir as coordenadas do primeiro bloco de cada caminho (CENTRO DO BLOCO)
        self.coordenadas_inicio_caminho = {
            # Amarelo (0) - Começa à direita da caixa 100x100
            0: (50 + 100 + self.tamanho_bloco // 2, 50 + self.tamanho_bloco // 2), 
            # Roxo (1) - Começa abaixo da caixa 100x100
            1: (LARGURA_TELA - 50 - self.tamanho_bloco // 2, 50 + 100 + self.tamanho_bloco // 2),
            # Rosa (2) - Começa à direita da caixa 100x100
            2: (50 + 100 + self.tamanho_bloco // 2, ALTURA_TELA - 50 - self.tamanho_bloco // 2), 
            # Azul (3) - Começa acima da caixa 100x100
            3: (LARGURA_TELA - 50 - self.tamanho_bloco // 2, ALTURA_TELA - 50 - 100 - self.tamanho_bloco // 2),
        }

    def _desenhar_moedas(self, screen, x, y, cor_fundo, num_moedas):
        """Desenha as moedas (círculos '3') sobre a imagem do porquinho."""
        
        posicoes = [(-20, -20), (0, -20), (20, -20), 
                    (-20, 0), (0, 0), (20, 0)]
        
        moedas_a_desenhar = min(num_moedas, TOTAL_MOEDAS_INICIAIS) 
        
        for i in range(moedas_a_desenhar):
            moeda_x = x + posicoes[i][0] + 35 
            moeda_y = y + posicoes[i][1] + 35
            
            pygame.draw.circle(screen, cor_fundo, (moeda_x, moeda_y), 10)
            
            texto = self.font.render("3", True, COR_BRANCO)
            screen.blit(texto, (moeda_x - 5, moeda_y - 8))
            
    def _desenhar_porquinhos(self):
        """Desenha os 4 porquinhos e suas moedas."""
        
        asset_map = {0: "amarelo", 1: "roxo", 2: "rosa", 3: "azul"}
        
        for i, jogador in enumerate(self.game.jogadores):
            x_canto, y_canto = self.coordenadas_canto[i]
            
            # Desenha o bloco de cor do porquinho (Fundo)
            pygame.draw.rect(self.screen, jogador.cor, (x_canto, y_canto, 100, 100), 0, 5)

            # Desenha a imagem do porquinho 
            asset_nome = asset_map[i]
            porquinho_img = self.assets_carregados.get(asset_nome, self.placeholder_porco) 
            
            # Posições dos 4 porquinhos (simplificação, 2x2)
            pos_porcos = [
                (x_canto + 5, y_canto + 5), (x_canto + 50, y_canto + 5),
                (x_canto + 5, y_canto + 50), (x_canto + 50, y_canto + 50)
            ]
            
            num_porquinhos_visiveis = math.ceil(jogador.moedas_no_porco / MOEDAS_INICIAIS_POR_PORCO)
            
            for j in range(NUM_PORCOS):
                if j < num_porquinhos_visiveis:
                    self.screen.blit(porquinho_img, pos_porcos[j])
                else:
                    # Desenha um bloco vazio se o porquinho já depositou suas 3 moedas
                    pygame.draw.rect(self.screen, COR_PRETO, (pos_porcos[j][0], pos_porcos[j][1], 40, 40)) 


            # Desenha as moedas restantes no porco principal
            moedas_a_mostrar = num_porquinhos_visiveis
            self._desenhar_moedas(self.screen, x_canto, y_canto, jogador.cor, moedas_a_mostrar)


    def _desenhar_caminho(self):
        """Desenha os caminhos de blocos em forma de L para o centro."""
        
        for i, cor in enumerate(self.game.cores_tabuleiro):
            # Ponto de partida do primeiro bloco (centro do bloco 1)
            x_atual, y_atual = self.coordenadas_inicio_caminho[i]
            
            # Movimentos do caminho (9 passos)
            movimentos = self.path_movements[i]
            
            for dx_step, dy_step in movimentos:
                # O bloco_x e bloco_y representam o CENTRO do quadrado a ser desenhado
                bloco_x = x_atual
                bloco_y = y_atual
                
                # Desenha o quadrado (ajustando o canto superior esquerdo para centralizar)
                pygame.draw.rect(self.screen, cor, 
                                 (bloco_x - self.tamanho_bloco // 2, 
                                  bloco_y - self.tamanho_bloco // 2, 
                                  self.tamanho_bloco, self.tamanho_bloco))
                                  
                # Prepara as coordenadas para o próximo bloco (desloca o centro do bloco)
                x_atual += dx_step * self.unidade_passo # Usa UNIDADE_PASSO
                y_atual += dy_step * self.unidade_passo # Usa UNIDADE_PASSO
                                  
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
        
        for i, jogador in enumerate(self.game.jogadores):
            posicao_caminho = jogador.posicao_caminho
            
            # Posição 0: Fora do caminho (no canto)
            # Posições 1 a 9: No caminho colorido
            if posicao_caminho > 0 and posicao_caminho <= self.caminho_tamanho: 
                
                # Ponto de partida (centro do bloco 1)
                x_atual, y_atual = self.coordenadas_inicio_caminho[i]
                
                # Movimentos do caminho (9 passos)
                movimentos = self.path_movements[i]
                
                # Calcula a posição do centro do bloco (posicao_caminho)
                # O loop vai até posicao_caminho - 1, para parar na posição correta
                for j in range(posicao_caminho - 1): 
                    dx_step, dy_step = movimentos[j]
                    
                    x_atual += dx_step * self.unidade_passo # Usa UNIDADE_PASSO
                    y_atual += dy_step * self.unidade_passo # Usa UNIDADE_PASSO
                
                # (x_atual, y_atual) é o centro do bloco onde o jogador está
                pygame.draw.circle(self.screen, jogador.cor, (x_atual, y_atual), self.tamanho_bloco // 3)

            # Posição 10: No centro (chegou ao círculo branco)
            elif posicao_caminho == self.caminho_tamanho + 1: 
                # Desenha o indicador no centro do tabuleiro (sobre o círculo branco)
                pygame.draw.circle(self.screen, jogador.cor, (self.centro_x, self.centro_y), self.tamanho_bloco // 3) 
                
    def desenhar_tudo(self):
        """Desenha todos os elementos do jogo."""
        self._desenhar_caminho()
        self._desenhar_porquinhos()
        self._desenhar_centro()
        self._desenhar_indicadores()