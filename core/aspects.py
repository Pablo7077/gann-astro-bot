from __future__ import annotations
from core.astro_core import angular_distance

ASPECTS = {
    0: ('Conjunction', 6, 'VOLATILE', 6),
    60: ('Sextile', 4, 'BULLISH', 4),
    90: ('Square', 6, 'BEARISH', 6),
    120: ('Trine', 5, 'BULLISH', 5),
    180: ('Opposition', 7, 'BEARISH', 7),
}


def detect_aspects(positions):
    planets = list(positions.keys())
    found = []
    for i in range(len(planets)):
        for j in range(i+1, len(planets)):
            p1, p2 = planets[i], planets[j]
            dist = angular_distance(positions[p1]['longitude'], positions[p2]['longitude'])
            for exact, (name, orb, bias, weight) in ASPECTS.items():
                if abs(dist - exact) <= orb:
                    found.append({'planet1': p1, 'planet2': p2, 'aspect': name, 'distance': round(dist, 2), 'direction': bias, 'weight': weight})
    return found


def summarize_aspects(aspects):
    bull = sum(a['weight'] for a in aspects if a['direction'] == 'BULLISH')
    bear = sum(a['weight'] for a in aspects if a['direction'] == 'BEARISH')
    vol = sum(a['weight'] for a in aspects if a['direction'] == 'VOLATILE')
    bias = 'BULLISH' if bull > bear and bull >= vol else 'BEARISH' if bear > bull and bear >= vol else 'VOLATILE'
    return {'bullish': bull, 'bearish': bear, 'volatile': vol, 'bias': bias, 'count': len(aspects)}
