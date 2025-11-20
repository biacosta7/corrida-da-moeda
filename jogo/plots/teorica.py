import numpy as np
from scipy.stats import binom

def calcular_teorica(n):
    if n == 0:
        return np.array([1.0])  # P(X = 0) = 1
    
    k = np.arange(0, n+1)
    pmf = binom.pmf(k, n, 0.5)
    return pmf
