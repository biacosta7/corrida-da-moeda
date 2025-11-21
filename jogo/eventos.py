# eventos.py

import random

class SimuladorMoeda:
    """Gerencia a simulação estatística e os resultados da moeda."""
    def __init__(self):
        self.cara = 0
        self.coroa = 0
        self.total = 0
        
    def lancar_e_registrar(self):
        """Simula o lançamento, registra o resultado e retorna 'H' (Cara) ou 'T' (Coroa)."""
        resultado = random.choice(['H', 'T']) # PARA TESTAR: resultado = random.choices(['C', 'K'], weights=[80, 20], k=1)[0]
        self.total += 1
        
        if resultado == 'H':
            self.cara += 1
            return 'H'
        else:
            self.coroa += 1
            return 'T'

# Instância global para ser usada em grafico.py e corrida.py
sim = SimuladorMoeda()