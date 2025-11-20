# eventos.py
# interface simples para a simulação global (um único objeto compartilhado)
from simulacao import SimulacaoMoeda

sim = SimulacaoMoeda()

def lancar_moeda():
    return sim.lancar()

def obter_frequencias():
    return sim.get_frequencias()

def obter_contadores():
    return sim.get_counts()
