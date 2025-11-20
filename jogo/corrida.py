class Personagem:
    def __init__(self, nome):
        self.nome = nome
        self.x = 0
        self.pontuacao = 0
    
    def avancar(self):
        self.x += 5
        self.pontuacao += 1
