# corrida.py

import random
from assets import *
from eventos import sim

class Player:
    def __init__(self, id, cor):
        self.id = id
        self.cor = cor
        self.moedas_no_porco = TOTAL_MOEDAS_INICIAIS
        self.moedas_depositadas = 0
        self.posicao_caminho = 0  # 0: início, caminho_tamanho: centro

class GameManager:
    def __init__(self, num_jogadores=2):
        self.jogadores = [
            Player(0, COR_AMARELO),
            Player(1, COR_ROSA),
            # Adicione mais se for multi-jogador
        ]
        
        # Corrigindo as cores para os 4 jogadores do tabuleiro
        self.cores_tabuleiro = [COR_AMARELO, COR_ROSA, COR_AZUL, COR_ROXO]
        self.jogadores = [Player(i, self.cores_tabuleiro[i]) for i in range(4)]

        self.jogador_atual_idx = 0
        self.jogo_ativo = True
        self.vencedor = None
        self.tamanho_caminho = CAMINHO_TAMANHO
        
    def proximo_jogador(self):
        """Passa o turno para o próximo jogador."""
        self.jogador_atual_idx = (self.jogador_atual_idx + 1) % len(self.jogadores)

    def executar_turno(self):
        """Executa um turno: lança a moeda, move o jogador, verifica o depósito."""
        if not self.jogo_ativo:
            return

        jogador = self.jogadores[self.jogador_atual_idx]
        resultado = sim.lancar()
        
        # A regra de avanço: Cara avança, Coroa fica/recua (simplificação)
        # Vamos usar: Cara avança, Coroa recua
        if resultado == 'H':
            # Avança se não estiver no centro
            if jogador.posicao_caminho < self.tamanho_caminho:
                jogador.posicao_caminho += 1
        elif resultado == 'T':
            # Recua se não estiver no início
            if jogador.posicao_caminho > 0:
                jogador.posicao_caminho -= 1
        
        self._verificar_deposito(jogador)
        self._verificar_vitoria(jogador)
        
        if self.jogo_ativo:
            self.proximo_jogador()

    def _verificar_deposito(self, jogador):
        """Verifica se o jogador alcançou o centro e deposita uma moeda."""
        if jogador.posicao_caminho == self.tamanho_caminho:
            if jogador.moedas_no_porco > 0:
                jogador.moedas_no_porco -= 1
                jogador.moedas_depositadas += 1
                # Volta para o início após o depósito
                jogador.posicao_caminho = 0 
                print(f"Jogador {jogador.id} depositou moeda! Total: {jogador.moedas_depositadas}")
            else:
                # Se não tem moedas, mas está no centro, apenas volta
                jogador.posicao_caminho = 0

    def _verificar_vitoria(self, jogador):
        """Verifica se o jogador ganhou."""
        if jogador.moedas_depositadas == TOTAL_MOEDAS_INICIAIS:
            self.vencedor = jogador
            self.jogo_ativo = False
            print(f"FIM DE JOGO! Jogador {jogador.id} ({jogador.cor}) venceu!")