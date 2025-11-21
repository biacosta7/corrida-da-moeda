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
        
        # Placeholder genérico (Agora 40x40, o tamanho correto para o grid 2x2)
        self.placeholder_porco = pygame.Surface((40, 40)) 
        self.placeholder_porco.fill((100, 100, 100)) # Cor Cinza
        
        self.assets_carregados = {}

        for nome, nome_arquivo in ASSETS.items():
            
            caminho_completo = os.path.join(SCRIPT_DIR, nome_arquivo) 
            
            try:
                img = pygame.image.load(caminho_completo).convert_alpha()
                
                # Redimensionar e armazenar SOMENTE se o carregamento foi bem-sucedido
                if 'porco' in nome:
                    self.assets_carregados[nome] = pygame.transform.scale(img, (40, 40))
                elif nome == 'bag':
                    self.assets_carregados[nome] = pygame.transform.scale(img, (100, 100))
            
            except pygame.error as e:
                print(f"🛑 ERRO CRÍTICO AO CARREGAR IMAGEM: {nome_arquivo} em {caminho_completo}. Erro: {e}")
            
            # CONSTRUÇÃO DO CAMINHO: Junta o diretório do script (jogo/) 
            caminho_completo = os.path.join(SCRIPT_DIR, nome_arquivo) 
            
            try:
                img = pygame.image.load(caminho_completo).convert_alpha()
                
                # Redimensionar porquinhos e o saco
                if 'porco' in nome:
                    # PADRONIZAÇÃO: Escala para 40x40 para caber no grid 2x2.
                    self.assets_carregados[nome] = pygame.transform.scale(img, (40, 40))
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
        self.unidade_passo = UNIDADE_PASSO 
        self.caminho_tamanho = CAMINHO_TAMANHO 

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
        
        # Estrutura do Caminho (9 movimentos)
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
            0: (50 + 100 + self.unidade_passo // 2, 50 + self.unidade_passo // 2), 
            1: (LARGURA_TELA - 50 - self.unidade_passo // 2, 50 + 100 + self.unidade_passo // 2),
            2: (50 + 100 + self.unidade_passo // 2, ALTURA_TELA - 50 - self.unidade_passo // 2), 
            3: (LARGURA_TELA - 50 - self.unidade_passo // 2, ALTURA_TELA - 50 - 100 - self.unidade_passo // 2),
        }
        
        # constantes/limites usados pela interface
        self.MOEDAS_INICIAIS_POR_PORCO = 3
        self.NUM_PORCOS = 4

    def _desenhar_moedas(self, screen, x, y, total_moedas):
        """
        Desenha, para cada um dos 4 porquinhos (posição 2x2 dentro do bloco 100x100),
        quantas moedas esse porquinho tem (0..MOEDAS_INICIAIS_POR_PORCO).
        total_moedas é o total de moedas do jogador (ex: 7).
        """
        posicoes = [
            (25, 25), (75, 25),
            (25, 75), (75, 75)
        ]

        # Para cada porquinho (0..NUM_PORCOS-1) calcula quantas moedas ele tem
        for i in range(self.NUM_PORCOS):
            # moedas pertencentes ao porquinho i
            moedas_porquinho = max(0, min(total_moedas - i * self.MOEDAS_INICIAIS_POR_PORCO,
                                            self.MOEDAS_INICIAIS_POR_PORCO))

            if moedas_porquinho > 0:
                cx = x + posicoes[i][0]
                cy = y + posicoes[i][1]

                # Desenha o círculo de fundo e o número (3,2,1)
                pygame.draw.circle(screen, COR_BRANCO, (cx, cy), 10)
                texto = self.font.render(str(moedas_porquinho), True, COR_PRETO)
                screen.blit(
                    texto,
                    (cx - texto.get_width() // 2, cy - texto.get_height() // 2)
                )

    def _desenhar_porquinhos(self):
        """Desenha os 4 porquinhos e indica as moedas restantes."""
        
        asset_map = {
            0: "porco-amarelo", 
            1: "porco-roxo", 
            2: "porco-rosa", 
            3: "porco-azul"
        }
        
        for i, jogador in enumerate(self.game.jogadores):
            x_canto, y_canto = self.coordenadas_canto[i]
            
            # Desenha a área de fundo colorida do jogador (100x100)
            pygame.draw.rect(self.screen, jogador.cor, (x_canto, y_canto, 100, 100), 0, 15)

            asset_nome = asset_map[i]
            porquinho_img = self.assets_carregados.get(asset_nome, self.placeholder_porco)

            # Posições dos 4 porquinhos 2x2 dentro do bloco 100x100
            # As coordenadas estão ajustadas para imagens de 40x40
            pos_porcos = [
                (x_canto + 5, y_canto + 5), (x_canto + 55, y_canto + 5),
                (x_canto + 5, y_canto + 55), (x_canto + 55, y_canto + 55)
            ]
            
            # porquinhos_restantes: quantos porquinhos ainda têm moedas inteiras (3)
            porquinhos_restantes = 0
            
            if jogador.moedas_no_porco > 0:
                porquinhos_restantes = math.ceil(jogador.moedas_no_porco / self.MOEDAS_INICIAIS_POR_PORCO)

            for j in range(self.NUM_PORCOS):
                if j < porquinhos_restantes:
                    self.screen.blit(porquinho_img, pos_porcos[j])
                else:
                    # Se já foi depositado (lote vazio), desenha um bloco preto para mostrar que está esgotado
                    # O tamanho 40x40 é usado para cobrir o espaço do porquinho
                    pygame.draw.rect(self.screen, COR_PRETO, (pos_porcos[j][0], pos_porcos[j][1], 40, 40))
                    
            # Desenha os números (3,2,1,0) a partir do total de moedas do jogador
            self._desenhar_moedas(self.screen, x_canto, y_canto, jogador.moedas_no_porco)

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