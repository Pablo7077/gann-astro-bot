"""
=============================================================
🔮 GANN ASTRO BOT v1.0 — Main CLI Runner
=============================================================
Usage:
  python main.py                    # Interactive menu
  python main.py --quick            # Quick planetary analysis today
  python main.py --quick 2025-06-21 # Specific date
  python main.py --project nifty    # Full projection (today, Nifty)
  python main.py --project bitcoin 2025-09-22
  python main.py --levels 24000     # Gann SQ9 levels for price
  python main.py --angles 24000 18000 2023-03-20  # Gann angles
  python main.py --cycles 2024-06-04              # Time cycles from pivot
  python main.py --sectors          # Sector rotation
  python main.py --seasonal         # Seasonal dates
  python main.py --weekly nifty     # Weekly report
  python main.py --monthly nifty    # Monthly report
  python main.py --build nifty      # Build historical dataset
  python main.py --backtest nifty   # Run full backtest
  python main.py --symbols          # List all symbols
  python main.py --dashboard        # Launch web dashboard
=============================================================
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🔮  GANN ASTRO BOT v1.0  🔮                               ║
║                                                              ║
║   W.D. Gann Western Astrology + Market Analysis Engine       ║
║   Square of Nine · Gann Angles · Time Cycles                 ║
║   Planetary Aspects · Cardinal Ingresses · Sectors           ║
║                                                              ║
║   ⚠️  Research Tool Only — NOT Financial Advice              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

def mode_quick(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    from core.astro_engine import full_astro_analysis
    from core.aspects import detect_aspects, get_aspect_score
    from core.retrograde import retrograde_market_score

    analysis = full_astro_analysis(date_str)
    print(f"\n⚡ QUICK GANN ANALYSIS — {date_str}")
    print("=" * 60)
    print(f"\n🪐 PLANETARY POSITIONS (Tropical):")
    print(f"{'Planet':10s} {'Sign':14s} {'Deg':>7s} {'Dignity':12s} {'Retro'}")
    print("-" * 53)
    for name, d in analysis["positions"].items():
        r = "℞" if d["retrograde"] else ""
        print(f"{name:10s} {d['sign']:14s} {d['sign_degree']:6.2f}°  {d['dignity']:12s} {r}")

    aspects = detect_aspects(analysis["positions"])
    ascore  = get_aspect_score(aspects)
    print(f"\n🔗 ASPECTS: {len(aspects)} active | Bias: {ascore['bias']} ({ascore['confidence']}%)")
    for a in aspects[:5]:
        print(f"   {a['planet1']} – {a['planet2']:10s} {a['aspect']:14s} {a['market_signal']}")

    rscore = retrograde_market_score(date_str)
    print(f"\n℞ RETROGRADES: {', '.join(rscore['retrograde_planets']) or 'None'} | {rscore['market_signal']}")

def mode_projection(symbol="nifty", date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    from analysis.projector import generate_full_projection
    generate_full_projection(date_str, symbol)

def mode_levels(price):
    from core.gann_square import print_sq9_analysis
    print_sq9_analysis(float(price))

def mode_angles(current_price, pivot_price, pivot_date):
    from core.gann_angles import print_angle_analysis
    current_date = datetime.now().strftime("%Y-%m-%d")
    print_angle_analysis(float(current_price), current_date,
                          float(pivot_price), pivot_date)

def mode_cycles(pivot_date_str):
    from core.time_cycles import print_cycle_analysis
    print_cycle_analysis(pivot_date_str)

def mode_sectors(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    from core.astro_engine import get_planet_positions
    from core.sector_map import get_top_sectors
    pos = get_planet_positions(date_str)
    result = get_top_sectors(pos)
    print(f"\n🏭 SECTOR ROTATION — {date_str}")
    print("  📈 BULLISH:")
    for s in result["bullish_sectors"]:
        print(f"     {s['planet']:10s} ({s['dignity']:12s}) → {', '.join(s['sectors'][:2])}")
        print(f"       Stocks: {', '.join(s['key_stocks'])}")
    print("  📉 BEARISH:")
    for s in result["bearish_sectors"]:
        print(f"     {s['planet']:10s} ({s['dignity']:12s}) → {', '.join(s['sectors'][:2])}")

def mode_seasonal(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    from core.seasonal import print_seasonal
    print_seasonal(date_str)

def mode_weekly(symbol="nifty"):
    from reports.weekly_report import generate_weekly_report
    generate_weekly_report(symbol=symbol)

def mode_monthly(symbol="nifty"):
    from reports.monthly_report import generate_monthly_report
    generate_monthly_report(symbol=symbol)

def mode_build(symbol="nifty", start="2015-01-01"):
    from analysis.correlator import build_astro_market_dataset
    build_astro_market_dataset(symbol, start_date=start)

def mode_backtest(symbol="nifty"):
    from analysis.correlator import get_or_build_dataset
    from analysis.backtester import run_full_backtest
    df, name = get_or_build_dataset(symbol)
    if not df.empty:
        run_full_backtest(df, name)
    else:
        print("No dataset. Run --build first.")

def mode_symbols():
    from market.symbols import list_all_presets
    list_all_presets()

def mode_dashboard():
    print("🌐 Launching Streamlit Dashboard...")
    os.system("streamlit run dashboard/app.py")

def interactive_menu():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 Today: {today}\n")
    print("Choose what to do:")
    print("  1.  ⚡ Quick Analysis (today)")
    print("  2.  🔮 Full Projection (today, Nifty)")
    print("  3.  🔮 Full Projection (custom symbol/date)")
    print("  4.  📐 Gann Square of Nine Levels")
    print("  5.  📐 Gann Angle Analysis")
    print("  6.  ⏱️  Time Cycles from Pivot")
    print("  7.  🏭 Sector Rotation")
    print("  8.  🌞 Seasonal Analysis")
    print("  9.  📅 Weekly Report")
    print("  10. 📆 Monthly Report")
    print("  11. 🔨 Build Historical Dataset")
    print("  12. 📊 Run Deep Backtest")
    print("  13. 🌐 Launch Web Dashboard")
    print("  14. 📋 List All Symbols")

    choice = input("\nEnter choice (1-14): ").strip()

    if choice == "1":
        mode_quick()
    elif choice == "2":
        mode_projection("nifty")
    elif choice == "3":
        sym  = input("Symbol (nifty/bitcoin/AAPL/etc.): ").strip() or "nifty"
        d    = input(f"Date (YYYY-MM-DD) [default: {today}]: ").strip() or today
        mode_projection(sym, d)
    elif choice == "4":
        price = input("Enter price (e.g. 24000): ").strip()
        mode_levels(price)
    elif choice == "5":
        cp  = input("Current price: ").strip()
        pp  = input("Pivot price (major high or low): ").strip()
        pd_ = input("Pivot date (YYYY-MM-DD): ").strip()
        mode_angles(cp, pp, pd_)
    elif choice == "6":
        pd_ = input("Pivot date (YYYY-MM-DD): ").strip()
        mode_cycles(pd_)
    elif choice == "7":
        mode_sectors()
    elif choice == "8":
        mode_seasonal()
    elif choice == "9":
        sym = input("Symbol [nifty]: ").strip() or "nifty"
        mode_weekly(sym)
    elif choice == "10":
        sym = input("Symbol [nifty]: ").strip() or "nifty"
        mode_monthly(sym)
    elif choice == "11":
        sym = input("Symbol [nifty]: ").strip() or "nifty"
        start = input("Start date [2015-01-01]: ").strip() or "2015-01-01"
        mode_build(sym, start)
    elif choice == "12":
        sym = input("Symbol [nifty]: ").strip() or "nifty"
        mode_backtest(sym)
    elif choice == "13":
        mode_dashboard()
    elif choice == "14":
        mode_symbols()
    else:
        print("Invalid choice.")

def main():
    print_banner()
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "--quick":
            mode_quick(sys.argv[2] if len(sys.argv) > 2 else None)
        elif cmd == "--project":
            sym  = sys.argv[2] if len(sys.argv) > 2 else "nifty"
            date = sys.argv[3] if len(sys.argv) > 3 else None
            mode_projection(sym, date)
        elif cmd == "--levels":
            mode_levels(sys.argv[2] if len(sys.argv) > 2 else 24000)
        elif cmd == "--angles":
            mode_angles(sys.argv[2], sys.argv[3], sys.argv[4])
        elif cmd == "--cycles":
            mode_cycles(sys.argv[2] if len(sys.argv) > 2 else None)
        elif cmd == "--sectors":
            mode_sectors()
        elif cmd == "--seasonal":
            mode_seasonal()
        elif cmd == "--weekly":
            mode_weekly(sys.argv[2] if len(sys.argv) > 2 else "nifty")
        elif cmd == "--monthly":
            mode_monthly(sys.argv[2] if len(sys.argv) > 2 else "nifty")
        elif cmd == "--build":
            sym   = sys.argv[2] if len(sys.argv) > 2 else "nifty"
            start = sys.argv[3] if len(sys.argv) > 3 else "2015-01-01"
            mode_build(sym, start)
        elif cmd == "--backtest":
            mode_backtest(sys.argv[2] if len(sys.argv) > 2 else "nifty")
        elif cmd == "--symbols":
            mode_symbols()
        elif cmd == "--dashboard":
            mode_dashboard()
        else:
            print(f"Unknown command: {cmd}")
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
