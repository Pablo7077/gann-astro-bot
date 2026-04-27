from __future__ import annotations
import sys
from datetime import datetime
from analysis.projector import generate_projection
from reports.daily_report import generate_daily_report
from analysis.backtester import build_signal_dataset, analyze_backtest
from market.symbols import list_all_presets


def show_quick(date_str=None, symbol='nifty'):
    date_str = date_str or datetime.now().strftime('%Y-%m-%d')
    r = generate_projection(date_str, symbol)
    print(f"\nGANN MARKET BOT | {symbol.upper()} | {date_str}")
    print('=' * 60)
    print(f"Bias: {r['bias']}")
    print(f"Action: {r['action']}")
    print(f"Decision Tree: {r['decision_tree']}")
    print(f"Confidence: {r['confidence']}%")
    print(f"Bullish Score: {r['bullish_score']} | Bearish Score: {r['bearish_score']} | Volatile Score: {r['volatile_score']}")
    print('\nSignals:')
    for name, direction, weight, detail in r['signals']:
        print(f"- [{weight}] {direction}: {name} -> {detail}")


def run_backtest(symbol='nifty', start='2022-01-01'):
    df, name, ticker = build_signal_dataset(symbol, start=start)
    summary = analyze_backtest(df)
    print(f"\nBACKTEST | {name} ({ticker})")
    print('=' * 60)
    for k, v in summary.items():
        if isinstance(v, list):
            print(f"\n{k}:")
            for row in v:
                print(row)
        else:
            print(f"{k}: {v}")


def menu():
    print('\nChoose an option:')
    print('1. Quick analysis')
    print('2. Save daily report')
    print('3. Run backtest')
    print('4. List symbols')
    choice = input('Enter 1-4: ').strip()
    if choice == '1':
        symbol = input('Symbol [nifty]: ').strip() or 'nifty'
        date_str = input('Date YYYY-MM-DD [today]: ').strip() or datetime.now().strftime('%Y-%m-%d')
        show_quick(date_str, symbol)
    elif choice == '2':
        symbol = input('Symbol [nifty]: ').strip() or 'nifty'
        date_str = input('Date YYYY-MM-DD [today]: ').strip() or datetime.now().strftime('%Y-%m-%d')
        result = generate_daily_report(symbol, date_str, save=True)
        print(f"Saved: {result['report_path']}")
    elif choice == '3':
        symbol = input('Symbol [nifty]: ').strip() or 'nifty'
        start = input('Start date YYYY-MM-DD [2022-01-01]: ').strip() or '2022-01-01'
        run_backtest(symbol, start)
    elif choice == '4':
        list_all_presets()
    else:
        print('Invalid choice')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == '--quick':
            show_quick(sys.argv[2] if len(sys.argv) > 2 else None, sys.argv[3] if len(sys.argv) > 3 else 'nifty')
        elif cmd == '--report':
            result = generate_daily_report(sys.argv[2] if len(sys.argv) > 2 else 'nifty', sys.argv[3] if len(sys.argv) > 3 else None, save=True)
            print(result['report_path'])
        elif cmd == '--backtest':
            run_backtest(sys.argv[2] if len(sys.argv) > 2 else 'nifty', sys.argv[3] if len(sys.argv) > 3 else '2022-01-01')
        elif cmd == '--symbols':
            list_all_presets()
        else:
            menu()
    else:
        menu()
