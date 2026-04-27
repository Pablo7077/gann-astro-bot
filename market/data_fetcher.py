from __future__ import annotations
import pandas as pd
import yfinance as yf
from market.symbols import resolve_symbol

def get_market_data(user_input='nifty', start='2018-01-01', end=None, auto_adjust=True):
    ticker, display_name = resolve_symbol(user_input)
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=auto_adjust)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    if df.empty:
        return pd.DataFrame(), display_name, ticker
    df = df.rename_axis('Date').reset_index()
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df['ReturnPct'] = df['Close'].pct_change() * 100
    df['NextClose'] = df['Close'].shift(-1)
    df['NextReturnPct'] = (df['NextClose'] / df['Close'] - 1) * 100
    df['GapPct'] = (df['Open'] / df['Close'].shift(1) - 1) * 100
    return df, display_name, ticker
