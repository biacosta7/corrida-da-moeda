import numpy as np
from scipy.stats import binom

def calcular_teorica(n):
    if n == 0:
        return [0, 1]
    k = np.array([0, 1])
    return binom.pmf(k, n, 0.5)
