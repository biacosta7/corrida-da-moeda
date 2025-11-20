# config.py
# Constantes do jogo

FPS = 30

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

GAME_AREA_WIDTH = 780   # área esquerda para o tabuleiro
GRAPH_AREA_WIDTH = WINDOW_WIDTH - GAME_AREA_WIDTH

BOARD_TOP = 80
BOARD_LEFT = 50
CELL_SIZE = 40
NUM_CELLS = 20          # tamanho do caminho (mude se quiser)
BOARD_Y = 250

PLAYER_COLORS = [
    (66, 135, 245),   # azul
    (245, 66, 150),   # rosa
    (66, 245, 127),   # verde
    (245, 199, 66),   # amarelo
]

MAX_PLAYERS = 4

COIN_ANIM_FRAMES = 12   # quantos frames de "giro" até resultado
COIN_ANIM_MS = 600      # duração da animação em ms

FONT_NAME = "dejavusans"
