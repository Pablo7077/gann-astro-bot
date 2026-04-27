from __future__ import annotations
import math

def gann_sq9_levels(price: float, step: float = 0.125, levels: int = 4):
    root = math.sqrt(max(price, 0.0001))
    resistances = []
    supports = []
    for i in range(1, levels + 1):
        resistances.append({'level': i, 'price': round((root + i * step) ** 2, 2)})
        supports.append({'level': i, 'price': round(max((root - i * step) ** 2, 0), 2)})
    return {'resistance': resistances, 'support': supports}
