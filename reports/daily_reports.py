"""Daily Gann Astro Report Generator."""

import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_daily_report(symbol="nifty", date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    from analysis.projector import generate_full_projection
    result = generate_full_projection(date_str, symbol)

    lines = []
    lines.append(f"{'='*65}")
    lines.append(f"  GANN ASTRO BOT — DAILY REPORT")
    lines.append(f"  Symbol: {symbol.upper()} | Date: {date_str}")
    lines.append(f"{'='*65}")
    lines.append(f"  FINAL BIAS: {result['bias']}")
    lines.append(f"  CONFIDENCE: {result['confidence']}%")
    lines.append(f"")
    lines.append(f"  SIGNALS:")
    for name, direction, weight, detail in result["signals"]:
        prefix = "[B]" if direction == "BULLISH" else ("[S]" if direction == "BEARISH" else "[V]")
        lines.append(f"    {prefix} {name}: {detail}")
    lines.append(f"")
    lines.append(f"  DISCLAIMER: Research only. Not financial advice.")
    lines.append(f"{'='*65}")

    report_text = "\n".join(lines)
    filename = f"daily_{symbol}_{date_str}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\n📄 Daily report saved: {filepath}")
    return report_text

if __name__ == "__main__":
    generate_daily_report("nifty")
