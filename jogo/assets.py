# assets.py

import pygame

# Cores do tabuleiro (estritamente as da imagem)
COR_AMARELO = (255, 172, 0)    # #ffac00
COR_ROSA = (238, 92, 89)       # #ee5c59
COR_AZUL = (0, 175, 199)       # #00afc7
COR_ROXO = (203, 108, 230)     # #cb6ce6
COR_BRANCO = (255, 255, 255)
COR_PRETO = (0, 0, 0)
COR_INDICADOR = (255, 255, 255) # Bolinha do jogador

# Assets de Imagem
ASSETS = {
    "amarelo": "assets/porco-amarelo.png",
    "rosa": "assets/porco-rosa.png",
    "azul": "assets/porco-azul.png",
    "roxo": "assets/porco-roxo.png",
    "bag": "assets/bag.png"
}

# Configurações do Jogo
LARGURA_TELA = 800
ALTURA_TELA = 600
TAMANHO_BLOCO = 20
CAMINHO_TAMANHO = 5 # 5 blocos de cada lado
MOEDAS_INICIAIS_POR_PORCO = 3
NUM_PORCOS = 4
TOTAL_MOEDAS_INICIAIS = MOEDAS_INICIAIS_POR_PORCO * NUM_PORCOS