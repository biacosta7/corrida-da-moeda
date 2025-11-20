# eventos.py

import random

class SimuladorMoeda:
    """Gerencia a simulação e os resultados da moeda."""
    def __init__(self):
        self.cara = 0
        self.coroa = 0
        self.total = 0
        
    def lancar(self):
        """Simula o lançamento de uma moeda justa (0.5/0.5)."""
        resultado = random.choice(['H', 'T']) # H (Cara) ou T (Coroa)
        self.total += 1
        
        if resultado == 'H':
            self.cara += 1
            return 'H'
        else:
            self.coroa += 1
            return 'T'

# Instância global para ser usada em grafico.py e corrida.py
sim = SimuladorMoeda()