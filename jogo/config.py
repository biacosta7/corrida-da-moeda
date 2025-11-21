# config.py
# Constantes do jogo

FPS = 30

# NOVO TAMANHO DA TELA (proporção mais retangular/wide)
LARGURA_TELA = 1400 
ALTURA_TELA = 800

GAME_AREA_WIDTH = LARGURA_TELA # O tabuleiro ocupa toda a largura agora
GRAPH_AREA_WIDTH = 0            # Não estamos mais usando a área separada

# --- NOVAS CONSTANTES PARA TABULEIRO ---
# O novo bloco de jogador é 180x180. Vamos usar uma margem de 50px.
AREA_JOGADOR_LADO = 180 

# Posição central do saco de moedas
CENTER_X = LARGURA_TELA // 2
CENTER_Y = ALTURA_TELA // 2

# Tamanho do bloco do caminho (mantido ou ajustado para caber o novo layout)
TAMANHO_BLOCO = 40 
UNIDADE_PASSO = 60 # Ajustado para criar mais espaço entre os blocos (era 40)

# O caminho precisa ser mais curto devido ao bloco de 180px e ao aumento da UNIDADE_PASSO
# 180 (jogador) + 60 (margem) + 9 * 60 (caminho) = 780.
# O novo layout suporta caminhos mais curtos. Vamos manter CAMINHO_TAMANHO=9, mas ajustar o layout na interface.
CAMINHO_TAMANHO = 9 # Tamanho do caminho (e.g., 9 passos)

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