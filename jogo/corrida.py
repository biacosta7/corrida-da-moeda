# corrida.py

import random
from config_assets import *
from eventos import sim

class Player:
    def __init__(self, id, cor):
        self.id = id
        self.cor = cor
        self.moedas_no_porco = TOTAL_MOEDAS_INICIAIS
        self.moedas_depositadas = 0
        self.posicao_caminho = 0 # 0: início, CAMINHO_TAMANHO + 1: centro

class GameManager:
    def __init__(self, num_jogadores=4):
        self.cores_tabuleiro = [COR_AMARELO, COR_ROXO, COR_ROSA, COR_AZUL] 
        self.jogadores = [Player(i, self.cores_tabuleiro[i]) for i in range(4)]

        self.jogador_atual_idx = 0
        self.jogo_ativo = True
        self.vencedor = None
        self.tamanho_caminho = CAMINHO_TAMANHO
        self.simulacao = sim

    def lancar_moeda(self):
        return sim.lancar_e_registrar()   # já vem 'C' ou 'K'


    def mover_jogador_ativo(self, passos):
        """Move o jogador ativo à frente, se possível."""
        jogador = self.jogadores[self.jogador_atual_idx]
        
        nova_posicao = jogador.posicao_caminho + passos
        
        # O centro de depósito é CAMINHO_TAMANHO + 1
        posicao_maxima = self.tamanho_caminho + 1

        # Garante que o jogador não ultrapasse o centro.
        jogador.posicao_caminho = min(nova_posicao, posicao_maxima)

    def processar_movimento_e_deposito(self, resultado_moeda):
        """Processa o movimento do jogador e verifica depósito, MAS NÃO PASSA O TURNO."""
        
        if not self.jogo_ativo:
            return
            
        # 1. Movimento baseado no resultado
        if resultado_moeda == 'C':
            self.mover_jogador_ativo(1)
        # Coroa ('K') não faz nada, o jogador fica parado.
        
        # 2. Verifica o estado do jogo
        self._verificar_deposito(self.jogadores[self.jogador_atual_idx])
        self._verificar_vitoria(self.jogadores[self.jogador_atual_idx])

    def proximo_jogador(self):
        """Passa o turno para o próximo jogador."""
        self.jogador_atual_idx = (self.jogador_atual_idx + 1) % len(self.jogadores)

    def _verificar_deposito(self, jogador):
        """Verifica se o jogador alcançou o centro e deposita uma moeda."""
        # Se a posição é o centro (tamanho_caminho + 1)
        if jogador.posicao_caminho == self.tamanho_caminho + 1:
            if jogador.moedas_no_porco > 0:
                jogador.moedas_no_porco -= 1
                jogador.moedas_depositadas += 1
                # Volta para o início (posicao 0)
                jogador.posicao_caminho = 0 
                print(f"Jogador {jogador.id} depositou moeda! Total: {jogador.moedas_depositadas}")
            else:
                # Se não tem moedas, apenas volta
                jogador.posicao_caminho = 0

    def _verificar_vitoria(self, jogador):
        if jogador.moedas_depositadas == TOTAL_MOEDAS_INICIAIS:
            self.vencedor = jogador
            self.jogo_ativo = False
            print(f"FIM DE JOGO! Jogador {jogador.id} ({jogador.cor}) venceu!")