from __future__ import annotations

def get_seasonal_dates(year: int):
    return {
        'March Equinox': {'date': f'{year}-03-20', 'sign': 'Aries', 'market_note': 'New yearly impulse zone'},
        'June Solstice': {'date': f'{year}-06-21', 'sign': 'Cancer', 'market_note': 'Trend transition watch'},
        'September Equinox': {'date': f'{year}-09-22', 'sign': 'Libra', 'market_note': 'Balance / reversal watch'},
        'December Solstice': {'date': f'{year}-12-21', 'sign': 'Capricorn', 'market_note': 'Structure / pressure zone'},
    }
