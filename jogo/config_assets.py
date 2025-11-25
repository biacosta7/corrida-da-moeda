# assets.py
# Constantes do Jogo

FPS = 30

# --- DIMENSÕES DA TELA (MAIOR E RETANGULAR) ---
LARGURA_TELA = 1400
ALTURA_TELA = 800

# --- CONFIGURAÇÕES DO TABULEIRO ---
AREA_JOGADOR_LADO = 180 # Novo tamanho da área colorida do jogador
RAIO_CENTRO = 150        # Novo raio do círculo central
LADO_PORCO = 70         # Novo tamanho dos assets dos porquinhos (para caber no 180x180)
GAME_AREA_WIDTH = LARGURA_TELA # O tabuleiro ocupa toda a largura agora
GRAPH_AREA_WIDTH = 300            # Não estamos mais usando a área separada

TAMANHO_BLOCO = 40      # Lado do quadrado no caminho
UNIDADE_PASSO = 60      # Distância entre os centros dos blocos no caminho (era 40)
CAMINHO_TAMANHO = 9     # Número de passos no caminho (Blocos 1 a 9)

# Posição central do saco de moedas
CENTER_X = LARGURA_TELA // 2
CENTER_Y = ALTURA_TELA // 2

# --- ESTADO INICIAL DO JOGO ---
MOEDAS_POR_PORCO = 1    # Moedas por porquinho
NUM_PORCOS = 4          # Porquinhos por jogador
TOTAL_MOEDAS_INICIAIS = MOEDAS_POR_PORCO * NUM_PORCOS # 12 moedas
COR_INDICADOR = (255, 255, 255) # Branco

# --- CORES (RGB) ---
COR_PRETO = (0, 0, 0)
COR_BRANCO = (255, 255, 255)

# Cores dos Jogadores (e Caminhos)
COR_AMARELO = (245, 199, 66)
COR_ROXO = (153, 51, 204)
COR_ROSA = (245, 66, 150)
COR_AZUL = (66, 135, 245)

# --- ASSETS (Ajuste o caminho conforme sua estrutura de diretórios) ---
ASSETS = {
    "porco-amarelo": "assets/porco-amarelo.png",
    "porco-roxo": "assets/porco-roxo.png",
    "porco-rosa": "assets/porco-rosa.png",
    "porco-azul": "assets/porco-azul.png",
    "porco-preto": "assets/porco-preto.png",
    "bag": "assets/bag.png",
}

CELL_SIZE = 30 #40
NUM_CELLS = 7          # Tamanho do caminho (e.g., 7 casas por caminho, ajustado para caber bem)

# Cores dos caminhos na imagem (ajustadas para corresponder à imagem e aos índices)
PLAYER_COLORS = [
    (245, 199, 66),   # 0: Amarelo/Laranja (Caminho Superior)
    (245, 66, 150),   # 1: Rosa/Vermelho (Caminho Esquerdo)
    (153, 51, 204),   # 2: Roxo/Violeta (Caminho Direito)
    (66, 135, 245),   # 3: Azul (Caminho Inferior)
]

MAX_PLAYERS = 4

FONT_NAME = "dejavusans"
