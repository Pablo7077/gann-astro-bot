from __future__ import annotations
from datetime import datetime, timedelta

GANN_CYCLES = [30, 45, 60, 90, 120, 144, 180, 270, 360]

def get_cycle_dates(pivot_date: str, years_forward: int = 2):
    start = datetime.strptime(pivot_date, '%Y-%m-%d')
    out = []
    total_days = years_forward * 365
    for cycle in GANN_CYCLES:
        d = start + timedelta(days=cycle)
        while (d - start).days <= total_days:
            out.append({'cycle_days': cycle, 'date': d.strftime('%Y-%m-%d')})
            d += timedelta(days=cycle)
    out.sort(key=lambda x: x['date'])
    return out

def find_upcoming_cycles(pivot_date: str, current_date: str, window_days: int = 30):
    current = datetime.strptime(current_date, '%Y-%m-%d')
    all_dates = get_cycle_dates(pivot_date, years_forward=3)
    out = []
    for item in all_dates:
        d = datetime.strptime(item['date'], '%Y-%m-%d')
        delta = (d - current).days
        if 0 <= delta <= window_days:
            out.append({**item, 'days_away': delta})
    return out
