from __future__ import annotations
from datetime import datetime
import math

SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
SIGN_ELEMENTS = {'Aries':'Fire','Leo':'Fire','Sagittarius':'Fire','Taurus':'Earth','Virgo':'Earth','Capricorn':'Earth','Gemini':'Air','Libra':'Air','Aquarius':'Air','Cancer':'Water','Scorpio':'Water','Pisces':'Water'}
SIGN_QUALITIES = {'Aries':'Cardinal','Cancer':'Cardinal','Libra':'Cardinal','Capricorn':'Cardinal','Taurus':'Fixed','Leo':'Fixed','Scorpio':'Fixed','Aquarius':'Fixed','Gemini':'Mutable','Virgo':'Mutable','Sagittarius':'Mutable','Pisces':'Mutable'}
PLANET_SPEED = {'Sun':0.9856,'Moon':13.1764,'Mercury':1.2,'Venus':1.18,'Mars':0.524,'Jupiter':0.083,'Saturn':0.033,'Uranus':0.012,'Neptune':0.006,'Pluto':0.004}
PLANET_BASE = {'Sun':280,'Moon':218,'Mercury':250,'Venus':181,'Mars':355,'Jupiter':34,'Saturn':50,'Uranus':314,'Neptune':304,'Pluto':238}


def _days_since_epoch(date_str: str) -> int:
    return (datetime.strptime(date_str, '%Y-%m-%d') - datetime(2000,1,1)).days


def sign_of(longitude: float) -> str:
    return SIGNS[int(longitude // 30) % 12]


def sign_degree(longitude: float) -> float:
    return longitude % 30


def angular_distance(a: float, b: float) -> float:
    d = abs(a-b) % 360
    return min(d, 360-d)


def pseudo_planet_positions(date_str: str):
    days = _days_since_epoch(date_str)
    positions = {}
    for planet, base in PLANET_BASE.items():
        lon = (base + PLANET_SPEED[planet] * days) % 360
        retro = planet in {'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn'} and math.sin(days / (18 + len(planet))) < -0.92
        sign = sign_of(lon)
        positions[planet] = {
            'longitude': round(lon, 2),
            'sign': sign,
            'sign_degree': round(sign_degree(lon), 2),
            'element': SIGN_ELEMENTS[sign],
            'quality': SIGN_QUALITIES[sign],
            'retrograde': retro,
        }
    return positions


def full_analysis(date_str: str):
    positions = pseudo_planet_positions(date_str)
    fire = sum(1 for p in positions.values() if p['element'] == 'Fire')
    earth = sum(1 for p in positions.values() if p['element'] == 'Earth')
    air = sum(1 for p in positions.values() if p['element'] == 'Air')
    water = sum(1 for p in positions.values() if p['element'] == 'Water')
    return {
        'date': date_str,
        'positions': positions,
        'element_bias': {'Fire': fire, 'Earth': earth, 'Air': air, 'Water': water},
        'retrogrades': [k for k, v in positions.items() if v['retrograde']]
    }
