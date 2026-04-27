"""Monthly Gann Astro Report — all trading days in a month."""

import os
from datetime import datetime, timedelta
import calendar

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_monthly_report(symbol="nifty", year=None, month=None):
    now = datetime.now()
    if year is None:  year  = now.year
    if month is None: month = now.month

    from analysis.projector import generate_full_projection
    from core.time_cycles import seasonal_cycles
    from core.seasonal import find_next_ingresses

    lines = []
    lines.append(f"{'='*65}")
    lines.append(f"  GANN ASTRO BOT — MONTHLY REPORT")
    lines.append(f"  Symbol: {symbol.upper()} | Month: {calendar.month_name[month]} {year}")
    lines.append(f"{'='*65}\n")

    # Key seasonal dates
    seasonal = seasonal_cycles(year)
    month_seasonal = [s for s in seasonal if f"{year}-{month:02d}" in s["date"]]
    if month_seasonal:
        lines.append("  KEY SEASONAL DATES THIS MONTH:")
        for s in month_seasonal:
            lines.append(f"    {s['date']}  {s['name']:25s}  {s['notes']}")
        lines.append("")

    # Day-by-day projections
    lines.append("  DAILY PROJECTIONS:")
    lines.append(f"  {'Date':12s} {'Day':10s} {'Bias':25s} {'Conf':>6s}")
    lines.append("  " + "-" * 57)

    bull_days = 0; bear_days = 0; vol_days = 0
    num_days = calendar.monthrange(year, month)[1]
    for day in range(1, num_days + 1):
        date_obj = datetime(year, month, day)
        if date_obj.weekday() >= 5:
            continue  # Skip weekends
        date_str = date_obj.strftime("%Y-%m-%d")
        try:
            result = generate_full_projection(date_str, symbol)
            bias = result["bias"]
            conf = result["confidence"]
            icon = "🟢" if "BULL" in bias else ("🔴" if "BEAR" in bias else "🟡")
            lines.append(f"  {date_str}  {date_obj.strftime('%A'):10s} "
                         f"{icon} {bias:22s}  {conf:5.1f}%")
            if "BULL" in bias: bull_days += 1
            elif "BEAR" in bias: bear_days += 1
            else: vol_days += 1
        except Exception as e:
            lines.append(f"  {date_str}  ERROR: {e}")

    total = bull_days + bear_days + vol_days or 1
    lines.append(f"\n  MONTHLY SUMMARY:")
    lines.append(f"    Bullish days:  {bull_days} ({bull_days/total*100:.0f}%)")
    lines.append(f"    Bearish days:  {bear_days} ({bear_days/total*100:.0f}%)")
    lines.append(f"    Volatile days: {vol_days}  ({vol_days/total*100:.0f}%)")
    overall = "BULLISH" if bull_days > bear_days else ("BEARISH" if bear_days > bull_days else "MIXED")
    lines.append(f"    Overall Month: {overall}")
    lines.append(f"\n  DISCLAIMER: Research only. Not financial advice.")
    lines.append(f"{'='*65}")

    report_text = "\n".join(lines)
    filename = f"monthly_{symbol}_{year}_{month:02d}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\n📄 Monthly report saved: {filepath}")
    print(report_text)
    return report_text

if __name__ == "__main__":
    generate_monthly_report("nifty")
