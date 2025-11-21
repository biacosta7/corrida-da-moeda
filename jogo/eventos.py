# eventos.py

import random

class SimuladorMoeda:
    """Gerencia a simulação e os resultados da moeda."""
    def __init__(self):
        self.cara = 0
        self.coroa = 0
        self.total = 0
        
    def lancar_e_registrar(self): # <--- NOVO MÉTODO
        """Simula o lançamento e registra o resultado."""
        
        # 'H' (Cara) ou 'T' (Coroa) para manter a compatibilidade com o gráfico
        resultado = random.choice(['H', 'T']) 
        self.total += 1
        
        if resultado == 'H':
            self.cara += 1
            return 'H'
        else:
            self.coroa += 1
            return 'T'

# Instância global para ser usada em grafico.py e corrida.py
sim = SimuladorMoeda()