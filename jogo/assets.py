# assets.py
# Constantes do Jogo

# --- DIMENSÕES DA TELA (MAIOR E RETANGULAR) ---
LARGURA_TELA = 1400
ALTURA_TELA = 800

# --- CONFIGURAÇÕES DO TABULEIRO ---
AREA_JOGADOR_LADO = 180 # Novo tamanho da área colorida do jogador
RAIO_CENTRO = 150        # Novo raio do círculo central
LADO_PORCO = 70         # Novo tamanho dos assets dos porquinhos (para caber no 180x180)

TAMANHO_BLOCO = 40      # Lado do quadrado no caminho
UNIDADE_PASSO = 60      # Distância entre os centros dos blocos no caminho (era 40)
CAMINHO_TAMANHO = 9     # Número de passos no caminho (Blocos 1 a 9)

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