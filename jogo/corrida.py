# corrida.py
class Jogador:
    def __init__(self, nome, cor, idx):
        self.nome = nome
        self.cor = cor
        self.posicao = 0
        self.ativo = True       # se ainda não chegou ao final
        self.colocacao = None   # 1,2,3,4 quando termina
        self.idx = idx          # índice (0..)
