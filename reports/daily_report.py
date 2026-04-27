from __future__ import annotations
import os
from datetime import datetime
from analysis.projector import generate_projection
OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_daily_report(symbol='nifty', date_str=None, save=True):
    date_str = date_str or datetime.now().strftime('%Y-%m-%d')
    result = generate_projection(date_str, symbol)
    lines = []
    lines.append('=' * 70)
    lines.append('GANN MARKET BOT — DAILY REPORT')
    lines.append('=' * 70)
    lines.append(f'Date: {date_str}')
    lines.append(f'Symbol: {symbol.upper()}')
    lines.append(f'Bias: {result["bias"]}')
    lines.append(f'Action: {result["action"]}')
    lines.append(f'Decision Tree: {result["decision_tree"]}')
    lines.append(f'Confidence: {result["confidence"]}%')
    lines.append('')
    lines.append('SIGNALS')
    lines.append('-' * 70)
    for name, direction, weight, detail in result['signals']:
        lines.append(f'{direction:10s} {name:20s} wt:{weight:4} | {detail}')
    text = '\n'.join(lines)
    path = os.path.join(OUTPUT_DIR, f'daily_{symbol}_{date_str}.txt')
    if save:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
    result['report_text'] = text
    result['report_path'] = path
    return result
