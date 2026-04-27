from __future__ import annotations
from datetime import datetime
from core.astro_core import full_analysis
from core.aspects import detect_aspects, summarize_aspects
from core.seasonal import get_seasonal_dates


def _element_signal(element_bias):
    fire_air = element_bias['Fire'] + element_bias['Air']
    earth_water = element_bias['Earth'] + element_bias['Water']
    if fire_air > earth_water:
        return ('Element Bias', 'BULLISH', 5, 'Fire/Air dominance suggests expansion and activity')
    elif earth_water > fire_air:
        return ('Element Bias', 'BEARISH', 5, 'Earth/Water dominance suggests caution and contraction')
    return ('Element Bias', 'VOLATILE', 3, 'Balanced elemental profile')


def _retrograde_signal(retrogrades):
    count = len(retrogrades)
    if count >= 3:
        return ('Retrogrades', 'VOLATILE', 6, f'{count} retrogrades increase noise and reversals')
    elif count == 2:
        return ('Retrogrades', 'BEARISH', 4, 'Two retrogrades increase friction')
    elif count == 1:
        return ('Retrogrades', 'NEUTRAL', 2, f'One retrograde active: {retrogrades[0]}')
    return ('Retrogrades', 'BULLISH', 3, 'No major retrograde friction')


def _seasonal_signal(date_str):
    y = int(date_str[:4])
    seasonal = get_seasonal_dates(y)
    if date_str in [v['date'] for v in seasonal.values()]:
        return ('Seasonal Pivot', 'VOLATILE', 6, 'Major seasonal turning point')
    month_day = date_str[5:]
    if month_day in ['03-20', '06-21', '09-22', '12-21']:
        return ('Seasonal Pivot', 'VOLATILE', 6, 'Major seasonal turning point')
    return ('Seasonal Background', 'NEUTRAL', 1, 'No major seasonal pivot today')


def generate_projection(date_str=None, symbol='nifty'):
    date_str = date_str or datetime.now().strftime('%Y-%m-%d')
    analysis = full_analysis(date_str)
    aspects = detect_aspects(analysis['positions'])
    aspect_summary = summarize_aspects(aspects)
    signals = []
    signals.append(_element_signal(analysis['element_bias']))
    signals.append(_retrograde_signal(analysis['retrogrades']))
    signals.append(_seasonal_signal(date_str))
    if aspect_summary['bias'] == 'BULLISH':
        signals.append(('Planetary Aspects', 'BULLISH', aspect_summary['bullish'], f"{aspect_summary['count']} active aspects"))
    elif aspect_summary['bias'] == 'BEARISH':
        signals.append(('Planetary Aspects', 'BEARISH', aspect_summary['bearish'], f"{aspect_summary['count']} active aspects"))
    else:
        signals.append(('Planetary Aspects', 'VOLATILE', max(aspect_summary['volatile'], 2), f"{aspect_summary['count']} active aspects"))
    bullish = sum(w for _, d, w, _ in signals if d == 'BULLISH')
    bearish = sum(w for _, d, w, _ in signals if d == 'BEARISH')
    volatile = sum(w for _, d, w, _ in signals if d == 'VOLATILE')
    if bullish > bearish and bullish >= volatile:
        bias = 'BULLISH'
        action = 'LONG'
    elif bearish > bullish and bearish >= volatile:
        bias = 'BEARISH'
        action = 'SHORT'
    else:
        bias = 'VOLATILE'
        action = 'NO TRADE'
    total = bullish + bearish + volatile
    confidence = round((max(bullish, bearish, volatile) / total) * 100, 1) if total else 0.0
    decision = 'FULL SIZE' if confidence >= 70 else 'HALF SIZE' if confidence >= 55 else 'SKIP' if confidence >= 40 else 'NO TRADE'
    return {
        'date': date_str,
        'symbol': symbol,
        'bias': bias,
        'action': action,
        'decision_tree': decision,
        'confidence': confidence,
        'bullish_score': bullish,
        'bearish_score': bearish,
        'volatile_score': volatile,
        'signals': signals,
        'positions': analysis['positions'],
        'retrogrades': analysis['retrogrades'],
        'element_bias': analysis['element_bias'],
        'aspects': aspects,
    }
