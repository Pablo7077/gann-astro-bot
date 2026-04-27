PRESETS = {
    'nifty': ('^NSEI', 'NIFTY 50'),
    'banknifty': ('^NSEBANK', 'BANK NIFTY'),
    'sensex': ('^BSESN', 'SENSEX'),
    'bitcoin': ('BTC-USD', 'Bitcoin'),
    'gold': ('GC=F', 'Gold Futures'),
    'silver': ('SI=F', 'Silver Futures'),
    'crude': ('CL=F', 'Crude Oil'),
    'sp500': ('^GSPC', 'S&P 500'),
    'nasdaq': ('^IXIC', 'NASDAQ Composite'),
    'aapl': ('AAPL', 'Apple'),
    'tsla': ('TSLA', 'Tesla'),
    'msft': ('MSFT', 'Microsoft'),
    'tcs': ('TCS.NS', 'TCS'),
    'reliance': ('RELIANCE.NS', 'Reliance Industries'),
    'hdfcbank': ('HDFCBANK.NS', 'HDFC Bank')
}

def resolve_symbol(user_input: str):
    if not user_input:
        return PRESETS['nifty']
    key = user_input.strip().lower()
    return PRESETS.get(key, (user_input.strip(), user_input.strip().upper()))

def list_all_presets():
    for key, (ticker, name) in PRESETS.items():
        print(f"{key:12s} -> {ticker:12s} | {name}")
