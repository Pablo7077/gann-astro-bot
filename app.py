from __future__ import annotations
from datetime import date
import pandas as pd
import streamlit as st
import plotly.express as px
from analysis.projector import generate_projection
from analysis.backtester import build_signal_dataset, analyze_backtest
from core.sq9 import gann_sq9_levels
from core.time_cycles import get_cycle_dates, find_upcoming_cycles

st.set_page_config(page_title='Gann Market Bot', page_icon='🔮', layout='wide')
st.title('🔮 Gann Market Bot')
st.caption('Modern-Western / Gann-style market research dashboard. Research only, not financial advice.')

with st.sidebar:
    symbol = st.text_input('Symbol', value='nifty')
    selected_date = st.date_input('Analysis date', value=date.today())
    start_date = st.date_input('Backtest start date', value=date(2022, 1, 1))
    price_input = st.number_input('Price for SQ9 levels', value=24000.0, step=100.0)
    pivot_date = st.date_input('Pivot date for time cycles', value=date(2024, 1, 1))

analysis_tab, backtest_tab, sq9_tab, cycles_tab = st.tabs(['Daily Analysis', 'Backtester', 'Square of Nine', 'Time Cycles'])

with analysis_tab:
    result = generate_projection(selected_date.strftime('%Y-%m-%d'), symbol)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Bias', result['bias'])
    c2.metric('Action', result['action'])
    c3.metric('Decision', result['decision_tree'])
    c4.metric('Confidence', f"{result['confidence']}%")
    st.subheader('Signals')
    signal_df = pd.DataFrame(result['signals'], columns=['Name', 'Direction', 'Weight', 'Detail'])
    st.dataframe(signal_df, use_container_width=True)
    st.subheader('Planet Positions')
    pos_rows = []
    for planet, d in result['positions'].items():
        pos_rows.append({'Planet': planet, 'Sign': d['sign'], 'Degree': d['sign_degree'], 'Element': d['element'], 'Quality': d['quality'], 'Retrograde': d['retrograde']})
    st.dataframe(pd.DataFrame(pos_rows), use_container_width=True)

with backtest_tab:
    if st.button('Run backtest', type='primary'):
        df, name, ticker = build_signal_dataset(symbol, start=start_date.strftime('%Y-%m-%d'))
        if df.empty:
            st.error('No market data was returned for this symbol.')
        else:
            summary = analyze_backtest(df)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric('Trades', summary['trades'])
            m2.metric('Hit Rate', f"{summary['hit_rate_pct']}%")
            m3.metric('Strategy Return', f"{summary['strategy_total_return_pct']}%")
            m4.metric('Buy & Hold', f"{summary['buy_hold_total_return_pct']}%")
            st.write('### Deep performance analysis')
            st.json(summary)
            chart_df = df[['Date', 'CumStrategy', 'CumBuyHold']].copy()
            chart_df = chart_df.melt(id_vars='Date', var_name='Series', value_name='CumulativeReturn')
            fig = px.line(chart_df, x='Date', y='CumulativeReturn', color='Series', title='Strategy vs Buy & Hold')
            st.plotly_chart(fig, use_container_width=True)
            st.write('### Raw signal history')
            st.dataframe(df.tail(300), use_container_width=True)

with sq9_tab:
    levels = gann_sq9_levels(price_input)
    c1, c2 = st.columns(2)
    c1.write('Resistance')
    c1.dataframe(pd.DataFrame(levels['resistance']), use_container_width=True)
    c2.write('Support')
    c2.dataframe(pd.DataFrame(levels['support']), use_container_width=True)

with cycles_tab:
    all_cycles = get_cycle_dates(pivot_date.strftime('%Y-%m-%d'), years_forward=2)
    upcoming = find_upcoming_cycles(pivot_date.strftime('%Y-%m-%d'), selected_date.strftime('%Y-%m-%d'), window_days=45)
    st.write('Upcoming cycles')
    st.dataframe(pd.DataFrame(upcoming), use_container_width=True)
    st.write('All projected cycle dates')
    st.dataframe(pd.DataFrame(all_cycles), use_container_width=True)
