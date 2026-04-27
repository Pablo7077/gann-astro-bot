"""Weekly Gann Astro Report — loops 5 trading days."""

import os
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_weekly_report(symbol="nifty", start_date=None):
    if start_date is None:
        today = datetime.now()
        # Go to most recent Monday
        start_date = today - timedelta(days=today.weekday())
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    from analysis.projector import generate_full_projection

    lines = []
    lines.append(f"{'='*65}")
    lines.append(f"  GANN ASTRO BOT — WEEKLY REPORT")
    lines.append(f"  Symbol: {symbol.upper()} | Week of: {start_date.strftime('%Y-%m-%d')}")
    lines.append(f"{'='*65}\n")

    for day_offset in range(5):  # Mon–Fri
        day = start_date + timedelta(days=day_offset)
        if day.weekday() >= 5:
            continue
        date_str = day.strftime("%Y-%m-%d")
        print(f"\n  Processing {date_str}...")
        result = generate_full_projection(date_str, symbol)
        bias_icon = "🟢" if "BULL" in result["bias"] else ("🔴" if "BEAR" in result["bias"] else "🟡")
        lines.append(f"  {date_str} ({day.strftime('%A'):10s})  "
                     f"{bias_icon} {result['bias']:25s}  "
                     f"Confidence: {result['confidence']}%")

    lines.append(f"\n  DISCLAIMER: Research only. Not financial advice.")
    lines.append(f"{'='*65}")

    report_text = "\n".join(lines)
    filename = f"weekly_{symbol}_{start_date.strftime('%Y-%m-%d')}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\n📄 Weekly report saved: {filepath}")
    print(report_text)
    return report_text

if __name__ == "__main__":
    generate_weekly_report("nifty")