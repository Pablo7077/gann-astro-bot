from __future__ import annotations
import pandas as pd
from analysis.projector import generate_projection
from market.data_fetcher import get_market_data


def build_signal_dataset(symbol='nifty', start='2022-01-01', end=None):
    df, display_name, ticker = get_market_data(symbol, start=start, end=end)
    if df.empty:
        return pd.DataFrame(), display_name, ticker
    rows = []
    for _, row in df.iterrows():
        date_str = pd.to_datetime(row['Date']).strftime('%Y-%m-%d')
        signal = generate_projection(date_str, symbol)
        tool_direction = signal['bias']
        next_ret = row.get('NextReturnPct')
        actual_direction = 'BULLISH' if pd.notna(next_ret) and next_ret > 0 else 'BEARISH' if pd.notna(next_ret) and next_ret < 0 else 'FLAT'
        if tool_direction == 'BULLISH':
            strategy_ret = next_ret if pd.notna(next_ret) else 0
        elif tool_direction == 'BEARISH':
            strategy_ret = -next_ret if pd.notna(next_ret) else 0
        else:
            strategy_ret = 0
        correct = ((tool_direction == 'BULLISH' and actual_direction == 'BULLISH') or (tool_direction == 'BEARISH' and actual_direction == 'BEARISH'))
        rows.append({
            'Date': row['Date'],
            'Close': row['Close'],
            'NextReturnPct': next_ret,
            'ToolBias': tool_direction,
            'ToolAction': signal['action'],
            'DecisionTree': signal['decision_tree'],
            'Confidence': signal['confidence'],
            'BullishScore': signal['bullish_score'],
            'BearishScore': signal['bearish_score'],
            'VolatileScore': signal['volatile_score'],
            'ActualDirection': actual_direction,
            'CorrectDirection': correct,
            'StrategyReturnPct': strategy_ret,
            'BuyHoldReturnPct': next_ret if pd.notna(next_ret) else 0,
        })
    out = pd.DataFrame(rows)
    if not out.empty:
        out['CorrectDirection'] = out['CorrectDirection'].fillna(False)
        out['CumStrategy'] = (1 + out['StrategyReturnPct'].fillna(0) / 100).cumprod() - 1
        out['CumBuyHold'] = (1 + out['BuyHoldReturnPct'].fillna(0) / 100).cumprod() - 1
    return out, display_name, ticker


def analyze_backtest(signal_df: pd.DataFrame):
    if signal_df.empty:
        return {}
    traded = signal_df[signal_df['ToolBias'].isin(['BULLISH', 'BEARISH'])].copy()
    wins = traded[(traded['StrategyReturnPct'] > 0)]
    losses = traded[(traded['StrategyReturnPct'] < 0)]
    hit_rate = round(traded['CorrectDirection'].mean() * 100, 2) if len(traded) else 0
    win_rate = round((len(wins) / len(traded)) * 100, 2) if len(traded) else 0
    avg_trade = round(traded['StrategyReturnPct'].mean(), 3) if len(traded) else 0
    total_return = round(signal_df['CumStrategy'].iloc[-1] * 100, 2)
    bh_return = round(signal_df['CumBuyHold'].iloc[-1] * 100, 2)
    max_drawdown = round(((1 + signal_df['CumStrategy']).cummax() - (1 + signal_df['CumStrategy'])).max() * 100, 2)
    by_bias = traded.groupby('ToolBias')['StrategyReturnPct'].agg(['count', 'mean', 'sum']).reset_index().to_dict(orient='records')
    by_decision = signal_df.groupby('DecisionTree')['StrategyReturnPct'].agg(['count', 'mean', 'sum']).reset_index().to_dict(orient='records')
    return {
        'rows': int(len(signal_df)),
        'trades': int(len(traded)),
        'hit_rate_pct': hit_rate,
        'win_rate_pct': win_rate,
        'avg_trade_return_pct': avg_trade,
        'strategy_total_return_pct': total_return,
        'buy_hold_total_return_pct': bh_return,
        'alpha_vs_buy_hold_pct': round(total_return - bh_return, 2),
        'max_drawdown_pct': max_drawdown,
        'bias_breakdown': by_bias,
        'decision_breakdown': by_decision,
    }
