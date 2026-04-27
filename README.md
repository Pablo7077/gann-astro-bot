# Gann Market Bot

A beginner-friendly local Python project that uses modern western / Gann-style astrology-inspired market timing ideas for research, analysis, reporting, and backtesting.

## What this project does
- Daily signal engine for a symbol like `nifty`, `AAPL`, `BTC-USD`
- Gann-style modules: aspects, seasonal points, time cycles, square-of-nine-style levels
- Backtester that compares tool signals with actual market data
- Streamlit dashboard for local use
- Text reports for daily, weekly, and monthly analysis

## Quick start
1. Install Python 3.11 from python.org.
2. Clone your repository with GitHub Desktop.
3. Open Terminal in the project folder.
4. Run:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python main.py --quick
   streamlit run app.py
   ```

## Project structure
- `core/` -> astrology + Gann analysis helpers
- `market/` -> market data fetch + symbol mapping
- `analysis/` -> projection engine + backtester
- `reports/` -> daily/weekly/monthly report generators
- `app.py` -> Streamlit dashboard
- `main.py` -> command line entry point

## Important note
This is a research tool, not financial advice.
