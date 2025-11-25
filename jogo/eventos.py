# eventos.py

import random

class SimuladorMoeda:
    """Gerencia a simulação estatística e os resultados da moeda."""
    def __init__(self):
        self.cara = 0
        self.coroa = 0
        self.total = 0
        
    def lancar_e_registrar(self):
        """Simula o lançamento, registra o resultado e retorna 'C' (Cara) ou 'K' (Coroa)."""
        resultado = random.choice(['C', 'K']) # PARA TESTAR: resultado = random.choices(['C', 'K'], weights=[80, 20], k=1)[0]
        self.total += 1
        
        if resultado == 'C':
            self.cara += 1
            return 'C'
        else:
            self.coroa += 1
            return 'K'

# Instância global para ser usada em grafico.py e corrida.py
sim = SimuladorMoeda()