# config.py
# Constantes do jogo

FPS = 30

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

GAME_AREA_WIDTH = 780   # área esquerda para o tabuleiro
GRAPH_AREA_WIDTH = WINDOW_WIDTH - GAME_AREA_WIDTH

# --- NOVAS CONSTANTES PARA TABULEIRO DE 4 CAMINHOS ---
# Posição central do saco de moedas
CENTER_X = GAME_AREA_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2

CELL_SIZE = 40
NUM_CELLS = 7          # Tamanho do caminho (e.g., 7 casas por caminho, ajustado para caber bem)

# ESTADO INICIAL DO JOGO
PIGGY_COINS_START = 3  # Moedas por porquinho
PIGGY_BANKS_START = 4  # Porquinhos por jogador
TOTAL_COINS_START = PIGGY_COINS_START * PIGGY_BANKS_START # 12 moedas

# Cores dos caminhos na imagem (ajustadas para corresponder à imagem e aos índices)
PLAYER_COLORS = [
    (245, 199, 66),   # 0: Amarelo/Laranja (Caminho Superior)
    (245, 66, 150),   # 1: Rosa/Vermelho (Caminho Esquerdo)
    (153, 51, 204),   # 2: Roxo/Violeta (Caminho Direito)
    (66, 135, 245),   # 3: Azul (Caminho Inferior)
]

MAX_PLAYERS = 4

COIN_ANIM_FRAMES = 12
COIN_ANIM_MS = 600

FONT_NAME = "dejavusans"