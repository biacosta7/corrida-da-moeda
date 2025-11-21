# interface.py

import pygame
import math
import os 
from assets import * # Importa as constantes, incluindo LARGURA_TELA/ALTURA_TELA
from corrida import GameManager

# Determina o diretório absoluto onde este script (interface.py) está
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class BoardDrawer:
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game = game_manager
        
        # --- NOVOS TAMANHOS ---
        self.LADO_JOGADOR = AREA_JOGADOR_LADO # 180
        self.RAIO_CENTRO = RAIO_CENTRO       # 90
        self.LADO_PORCO = LADO_PORCO         # 70
        self.RAIO_MOEDA_CONTADOR = 15        # Raio dos círculos (3, 2, 1)

        self.placeholder_porco = pygame.Surface((self.LADO_PORCO, self.LADO_PORCO)) 
        self.placeholder_porco.fill((100, 100, 100))
        self.assets_carregados = {}

        # Carregamento e Redimensionamento de Assets
        for nome, nome_arquivo in ASSETS.items():
            caminho_completo = os.path.join(SCRIPT_DIR, nome_arquivo) 
            
            try:
                img = pygame.image.load(caminho_completo).convert_alpha()
                
                if 'porco' in nome:
                    # Redimensiona para o novo tamanho LADO_PORCO
                    self.assets_carregados[nome] = pygame.transform.scale(img, (self.LADO_PORCO, self.LADO_PORCO))
                elif nome == 'bag':
                    # Redimensiona para caber no novo centro (160x160 para margem no raio 90)
                    self.assets_carregados[nome] = pygame.transform.scale(img, (160, 160))
            
            except pygame.error as e:
                print(f"Erro ao carregar imagem: {nome_arquivo}. Usando placeholder. Erro: {e}")
                if 'porco' in nome:
                    self.assets_carregados[nome] = self.placeholder_porco 
                elif nome == 'bag':
                    self.assets_carregados[nome] = pygame.transform.scale(self.placeholder_porco, (160, 160))

        self.font = pygame.font.Font(None, 24)
        self.font_moedas = pygame.font.Font(None, 36)
        self.tamanho_bloco = TAMANHO_BLOCO
        self.unidade_passo = UNIDADE_PASSO 
        self.caminho_tamanho = CAMINHO_TAMANHO 

        # --- AJUSTE NO POSICIONAMENTO PARA LADO=180 ---
        MARGEM = 50 
        LADO = self.LADO_JOGADOR

        self.coordenadas_canto = {
            0: (MARGEM, MARGEM), # Amarelo (Superior Esquerdo)
            1: (LARGURA_TELA - MARGEM - LADO, MARGEM), # Roxo (Superior Direito)
            2: (MARGEM, ALTURA_TELA - MARGEM - LADO), # Rosa (Inferior Esquerdo)
            3: (LARGURA_TELA - MARGEM - LADO, ALTURA_TELA - MARGEM - LADO), # Azul (Inferior Direito)
        }
        
        self.centro_x = LARGURA_TELA // 2
        self.centro_y = ALTURA_TELA // 2
        
        # Estrutura do Caminho
        self.path_movements = {
            # 0: Amarelo (Inalterado: 7 Direita, 2 Baixo)
            0: [(1, 0)] * 7 + [(0, 1)] * 2,
            
            # 1: Roxo (3 para Baixo, 6 para Esquerda)
            1: [(0, 1)] * 2 + [(-1, 0)] * 7,
            
            # 2: Rosa (3 para Cima, 6 para Direita)
            2: [(0, -1)] * 2 + [(1, 0)] * 7,
            
            # 3: Azul (Inalterado: 7 Esquerda, 2 Cima)
            3: [(-1, 0)] * 7 + [(0, -1)] * 2,
        }
        
        # Coordenadas do primeiro bloco do caminho (CENTRO DO BLOCO)
        self.coordenadas_inicio_caminho = {
            # 0: Amarelo (Superior Esquerdo) - Começa à DIREITA do bloco (Correto para L-path)
            0: (MARGEM + LADO + self.unidade_passo // 2, MARGEM + LADO // 2), 
            
            # 1: Roxo (Superior Direito) - Começa ABAIXO do bloco (Correto para L-path)
            1: (LARGURA_TELA - MARGEM - LADO // 2, MARGEM + LADO + self.unidade_passo // 2),
            
            # 2: Rosa (Inferior Esquerdo) - Começa no topo, CENTRO do bloco, movendo para CIMA.
            2: (MARGEM + LADO // 2, ALTURA_TELA - MARGEM - LADO - self.unidade_passo // 2), 
            
            # 3: Azul (Inferior Direito) - Começa na lateral esquerda, CENTRO do bloco, movendo para ESQUERDA.
            3: (LARGURA_TELA - MARGEM - LADO - self.unidade_passo // 2, ALTURA_TELA - MARGEM - LADO // 2),
        }
                
        # Coordenadas centrais para o botão da moeda (Raio 90)
        self.RAIO_MOEDA_BOTAO = 20 # 90
        OFFSET_MOEDA = 100 # Offset para centralizar visualmente a moeda no espaço entre o bloco e o caminho

        self.coordenadas_moeda_botao = {
            # 0: Amarelo (Superior Esquerdo) -> Borda direita do bloco + raio do botão
            0: (MARGEM + LADO + self.RAIO_MOEDA_BOTAO, MARGEM + LADO // 2), 
            
            # 1: Roxo (Superior Direito) -> Borda esquerda do bloco - raio do botão
            1: (LARGURA_TELA - MARGEM - LADO - self.RAIO_MOEDA_BOTAO, MARGEM + LADO // 2),
            
            # 2: Rosa (Inferior Esquerdo) -> Borda inferior do bloco + raio do botão
            # O bloco 2 está no canto inferior esquerdo. O botão deve ficar à direita, como o jogador 0.
            # O posicionamento anterior colocava acima/abaixo, vamos seguir o padrão lateral para consistência visual.
            2: (MARGEM + LADO + self.RAIO_MOEDA_BOTAO, ALTURA_TELA - MARGEM - LADO // 2),
            
            # 3: Azul (Inferior Direito) -> Borda esquerda do bloco - raio do botão
            3: (LARGURA_TELA - MARGEM - LADO - self.RAIO_MOEDA_BOTAO, ALTURA_TELA - MARGEM - LADO // 2),
        }
        
        self.resultado_texto = ""

    def _desenhar_moedas(self, screen, x, y, total_moedas):
        """Desenha os contadores de moedas (3,2,1) dentro de cada porquinho."""
        
        # Posições 2x2 dentro do bloco 180x180 (distância entre centros 90px)
        posicoes = [
            (45, 45), (135, 45),
            (45, 135), (135, 135)
        ]

        for i in range(NUM_PORCOS):
            moedas_porquinho = max(0, min(total_moedas - i * MOEDAS_POR_PORCO, MOEDAS_POR_PORCO))

            if moedas_porquinho > 0:
                cx = x + posicoes[i][0]
                cy = y + posicoes[i][1]

                texto = self.font_moedas.render(str(moedas_porquinho), True, COR_PRETO) 
                screen.blit(
                    texto,
                    (cx - texto.get_width() // 2, cy - texto.get_height() // 2)
                )

    def _desenhar_porquinhos(self):
        """Desenha os 4 porquinhos e indica as moedas restantes."""
        asset_map = {0: "porco-amarelo", 1: "porco-roxo", 2: "porco-rosa", 3: "porco-azul"}
        
        for i, jogador in enumerate(self.game.jogadores):
            x_canto, y_canto = self.coordenadas_canto[i]
            
            # Desenha a área de fundo colorida do jogador (180x180)
            pygame.draw.rect(self.screen, jogador.cor, (x_canto, y_canto, self.LADO_JOGADOR, self.LADO_JOGADOR), 0, 25)

            asset_nome = asset_map[i]
            porquinho_img = self.assets_carregados.get(asset_nome, self.placeholder_porco)

            # Posições dos 4 porquinhos 2x2 dentro do bloco 180x180 (70x70)
            pos_porcos = [
                (x_canto + 10, y_canto + 10), (x_canto + 100, y_canto + 10),
                (x_canto + 10, y_canto + 100), (x_canto + 100, y_canto + 100)
            ]
            
            porquinhos_restantes = 0
            if jogador.moedas_no_porco > 0:
                porquinhos_restantes = math.ceil(jogador.moedas_no_porco / MOEDAS_POR_PORCO)

            for j in range(NUM_PORCOS):
                if j < porquinhos_restantes:
                    self.screen.blit(porquinho_img, pos_porcos[j])
                else:
                    # Bloco preto para porquinhos esgotados
                    pygame.draw.rect(self.screen, COR_PRETO, (pos_porcos[j][0], pos_porcos[j][1], self.LADO_PORCO, self.LADO_PORCO))
                    
            self._desenhar_moedas(self.screen, x_canto, y_canto, jogador.moedas_no_porco)

    def _desenhar_caminho(self):
        """Desenha os caminhos de blocos em forma de L para o centro."""
        
        for i, cor in enumerate(self.game.cores_tabuleiro):
            x_atual, y_atual = self.coordenadas_inicio_caminho[i]
            movimentos = self.path_movements[i]
            
            for dx_step, dy_step in movimentos:
                bloco_x = x_atual
                bloco_y = y_atual
                
                # Desenha o quadrado
                pygame.draw.rect(self.screen, cor, 
                                 (bloco_x - self.tamanho_bloco // 2, 
                                  bloco_y - self.tamanho_bloco // 2, 
                                  self.tamanho_bloco, self.tamanho_bloco))
                                  
                # Prepara as coordenadas para o próximo bloco
                x_atual += dx_step * self.unidade_passo
                y_atual += dy_step * self.unidade_passo
                        
    def _desenhar_centro(self):
        """Desenha o círculo central (raio 90) e o saco de moedas."""
        
        pygame.draw.circle(self.screen, COR_BRANCO, (self.centro_x, self.centro_y), self.RAIO_CENTRO) 
        
        # Saco de Moedas (BAG) 
        bag_img = self.assets_carregados.get('bag')
        self.screen.blit(bag_img, (self.centro_x - bag_img.get_width() // 2, self.centro_y - bag_img.get_height() // 2))
        
        # Desenhar os contadores de moedas depositadas
        raio_contador = 80 
        font_grande = pygame.font.Font(None, 48) 
        
        for i, jogador in enumerate(self.game.jogadores):
            pos_relativa = {
                0: (-raio_contador, -raio_contador), 
                1: (raio_contador, -raio_contador), 
                2: (-raio_contador, raio_contador), 
                3: (raio_contador, raio_contador), 
            }
            
            offset_x, offset_y = pos_relativa[i]
            contador_x = self.centro_x + offset_x
            contador_y = self.centro_y + offset_y

            texto = font_grande.render(str(jogador.moedas_depositadas), True, jogador.cor)
            self.screen.blit(texto, (contador_x - texto.get_width() // 2, 
                                     contador_y - texto.get_height() // 2))

    def _desenhar_indicadores(self):
        """Desenha as bolinhas que representam os jogadores nos caminhos."""
        
        for i, jogador in enumerate(self.game.jogadores):
            posicao_caminho = jogador.posicao_caminho
            
            if 0 < posicao_caminho <= self.caminho_tamanho: 
                x_atual, y_atual = self.coordenadas_inicio_caminho[i]
                movimentos = self.path_movements[i]
                
                for j in range(posicao_caminho - 1): 
                    dx_step, dy_step = movimentos[j]
                    x_atual += dx_step * self.unidade_passo
                    y_atual += dy_step * self.unidade_passo
                
                pygame.draw.circle(self.screen, COR_INDICADOR, (x_atual, y_atual), self.tamanho_bloco // 3)

            elif posicao_caminho == self.caminho_tamanho + 1: 
                # Posição no centro
                pygame.draw.circle(self.screen, jogador.cor, (self.centro_x, self.centro_y), self.tamanho_bloco // 3) 
                
    def _desenhar_moeda_botao(self):
        """Desenha a moeda clicável (raio 90) e o resultado (C/K) para o jogador ativo."""
        
        if not self.game.jogo_ativo:
            return

        jogador_ativo_idx = self.game.jogador_atual_idx
        cx, cy = self.coordenadas_moeda_botao[jogador_ativo_idx]
        raio = self.RAIO_MOEDA_BOTAO
        
        # 1. Desenhar Círculo de fundo preenchido
        cor_jogador = self.game.jogadores[jogador_ativo_idx].cor 
        pygame.draw.circle(self.screen, cor_jogador, (cx, cy), raio, 0)

        # 3. Desenhar o texto do resultado (C ou K)
        if self.resultado_texto:
            font_moeda = pygame.font.Font(None, 30) 
            texto = font_moeda.render(self.resultado_texto, True, COR_BRANCO)
            self.screen.blit(
                texto,
                (cx - texto.get_width() // 2, cy - texto.get_height() // 2)
            )
    
    def desenhar_tudo(self):
        """Desenha todos os elementos do jogo."""
        self._desenhar_caminho()
        self._desenhar_porquinhos()
        self._desenhar_centro()
        self._desenhar_indicadores()
        self._desenhar_moeda_botao()