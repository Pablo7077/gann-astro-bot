"""
============================================================
 Gann Astro Bot — Streamlit Web Dashboard
============================================================
 Run with:  streamlit run dashboard/app.py
============================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import datetime, date

st.set_page_config(
    page_title="Gann Astro Bot",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔮 Gann Astro Bot — Market Analysis Engine")
st.caption("W.D. Gann Western Astrology + Modern Market Data | ⚠️ Research Tool Only — Not Financial Advice")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    symbol = st.text_input("Symbol", value="nifty",
                            help="nifty, banknifty, bitcoin, gold, AAPL, etc.")
    selected_date = st.date_input("Analysis Date", value=date.today())
    date_str = selected_date.strftime("%Y-%m-%d")
    st.divider()
    st.caption("Supported: nifty, banknifty, bitcoin, gold, silver, crude, sp500, nasdaq, AAPL, TSLA, reliance, tcs, hdfcbank ...")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Daily Projection",
    "📐 Gann Levels",
    "⏱️ Time Cycles",
    "🏭 Sector Rotation",
    "📈 Backtester",
    "🌞 Seasonal",
])

# ── Tab 1: Daily Projection ────────────────────────────────────────────────
with tab1:
    st.subheader(f"Daily Gann Projection — {symbol.upper()} | {date_str}")
    if st.button("🔮 Generate Projection", type="primary", key="proj"):
        with st.spinner("Computing planetary positions and Gann signals..."):
            try:
                from analysis.projector import generate_full_projection
                result = generate_full_projection(date_str, symbol)

                bias = result["bias"]
                conf = result["confidence"]
                color = "green" if "BULL" in bias else ("red" if "BEAR" in bias else "orange")

                col1, col2, col3 = st.columns(3)
                col1.metric("Final Bias", bias)
                col2.metric("Confidence", f"{conf}%")
                col3.metric("Bull Score / Bear Score",
                            f"{result['bullish_score']} / {result['bearish_score']}")

                st.divider()
                st.subheader("📋 Signal Breakdown")
                for name, direction, weight, detail in result["signals"]:
                    icon = "🟢" if direction == "BULLISH" else ("🔴" if direction == "BEARISH" else "🟡")
                    st.write(f"{icon} **[{weight}]** {name} — {detail}")

                if result["warnings"]:
                    for w in result["warnings"]:
                        st.warning(w)

            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Make sure you've installed all requirements: pip install -r requirements.txt")

    # Planetary positions table
    st.subheader("🪐 Planetary Positions (Tropical)")
    if st.button("Show Positions", key="pos"):
        with st.spinner("Loading planetary data..."):
            try:
                from core.astro_engine import full_astro_analysis
                analysis = full_astro_analysis(date_str)
                import pandas as pd
                rows = []
                for name, d in analysis["positions"].items():
                    rows.append({
                        "Planet": name,
                        "Sign": d["sign"],
                        "Degree": f"{d['sign_degree']:.2f}°",
                        "Element": d["element"],
                        "Quality": d["quality"],
                        "Dignity": d["dignity"],
                        "Score": d["dignity_score"],
                        "Retrograde": "℞" if d["retrograde"] else "",
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True)
                st.write(f"**Retrogrades:** {', '.join(analysis['retrogrades']) or 'None'}")
                st.write(f"**Element Bias:** {analysis['element_bias']}")
            except Exception as e:
                st.error(f"Error: {e}")

# ── Tab 2: Gann Price Levels ──────────────────────────────────────────────
with tab2:
    st.subheader("📐 Gann Price Levels")
    price_input = st.number_input("Enter Price", min_value=1.0, value=24000.0, step=100.0)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Calculate SQ9 Levels"):
            from core.gann_square import gann_sq9_levels
            levels = gann_sq9_levels(price_input)
            import pandas as pd
            res_df = pd.DataFrame(levels["resistance"])
            sup_df = pd.DataFrame(levels["support"])
            st.write("**🔴 Resistance Levels:**")
            st.dataframe(res_df, use_container_width=True)
            st.write("**🟢 Support Levels:**")
            st.dataframe(sup_df, use_container_width=True)

    with col2:
        st.subheader("Gann Angle Calculator")
        pivot_p = st.number_input("Pivot Price", value=18000.0, step=100.0)
        pivot_d = st.date_input("Pivot Date", value=date(2023, 3, 20))
        price_unit = st.number_input("Price Unit", value=100.0, help="Gann unit per degree")
        direction = st.selectbox("Direction", ["up", "down"])

        if st.button("Calculate Angles"):
            from core.gann_angles import analyze_price_vs_angles
            result = analyze_price_vs_angles(
                price_input, date_str,
                pivot_p, pivot_d.strftime("%Y-%m-%d"),
                price_unit, direction
            )
            import pandas as pd
            angle_rows = [{"Angle": k, "Price": v,
                           "Above/Below": "↑ Above" if v > price_input else "↓ Below"}
                          for k, v in result["angle_prices"].items()]
            st.dataframe(pd.DataFrame(angle_rows).sort_values("Price"), use_container_width=True)
            st.info(f"**Position:** {result.get('between','')}")
            st.info(f"**Bias:** {result.get('bias','')}")

# ── Tab 3: Time Cycles ────────────────────────────────────────────────────
with tab3:
    st.subheader("⏱️ Gann Time Cycles from Major Pivot")
    pivot_date_input = st.date_input("Major Pivot Date (High or Low)",
                                      value=date(2024, 6, 4))
    years_fwd = st.slider("Project Forward (years)", 1, 5, 2)
    window = st.slider("Upcoming Window (days)", 7, 60, 30)

    if st.button("Calculate Time Cycles"):
        from core.time_cycles import get_cycle_dates, find_upcoming_cycles
        import pandas as pd
        pivot_str = pivot_date_input.strftime("%Y-%m-%d")
        upcoming = find_upcoming_cycles(pivot_str, date_str, window_days=window)
        all_cycles = get_cycle_dates(pivot_str, years_forward=years_fwd)

        if upcoming:
            st.warning(f"⭐ {len(upcoming)} cycle(s) hitting within {window} days!")
            st.dataframe(pd.DataFrame(upcoming), use_container_width=True)
        else:
            st.info(f"No cycle dates within {window} days of {date_str}")

        st.subheader("All Projected Cycle Dates")
        st.dataframe(pd.DataFrame(all_cycles[:30]), use_container_width=True)

# ── Tab 4: Sector Rotation ─────────────────────────────────────────────────
with tab4:
    st.subheader("🏭 Sector Rotation (Planetary-Based)")
    if st.button("Show Sector Signals"):
        with st.spinner("Analyzing sectors..."):
            try:
                from core.astro_engine import get_planet_positions
                from core.sector_map import get_top_sectors
                import pandas as pd
                pos = get_planet_positions(date_str)
                result = get_top_sectors(pos)

                col1, col2 = st.columns(2)
                with col1:
                    st.success("📈 BULLISH Sectors")
                    for s in result["bullish_sectors"]:
                        st.write(f"**{s['planet']}** ({s['dignity']}) → {', '.join(s['sectors'][:2])}")
                        st.caption(f"Stocks: {', '.join(s['key_stocks'])}")
                with col2:
                    st.error("📉 BEARISH Sectors")
                    for s in result["bearish_sectors"]:
                        st.write(f"**{s['planet']}** ({s['dignity']}) → {', '.join(s['sectors'][:2])}")
                        st.caption(f"Stocks: {', '.join(s['key_stocks'])}")

                st.subheader("All Planet Signals")
                rows = [{"Planet": s["planet"], "Dignity": s["dignity"],
                         "Score": s["dignity_score"], "Retro": s["retrograde"],
                         "Bias": s["bias"], "Sectors": ", ".join(s["sectors"][:2])}
                        for s in result["all_signals"]]
                st.dataframe(pd.DataFrame(rows), use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

# ── Tab 5: Backtester ─────────────────────────────────────────────────────
with tab5:
    st.subheader("📈 Deep Gann Astro Backtester")
    st.warning("⏳ First run downloads data & computes astro factors — may take 5–15 minutes.")

    start_date = st.date_input("Start Date", value=date(2018, 1, 1))
    if st.button("🚀 Run Backtest", type="primary"):
        with st.spinner("Downloading data and running backtest..."):
            try:
                from analysis.correlator import build_astro_market_dataset
                from analysis.backtester import run_full_backtest
                import io, contextlib

                df, name = build_astro_market_dataset(
                    symbol, start_date=start_date.strftime("%Y-%m-%d"))

                if df.empty:
                    st.error("No data retrieved. Check your symbol.")
                else:
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        result = run_full_backtest(df, name)
                    output = buf.getvalue()
                    st.text(output)

                    # Show top signals as table
                    import pandas as pd
                    if result.get("top_bullish"):
                        st.subheader("🏆 Top Bullish Signals")
                        st.dataframe(pd.DataFrame(result["top_bullish"]), use_container_width=True)
                    if result.get("top_bearish"):
                        st.subheader("🏆 Top Bearish Signals")
                        st.dataframe(pd.DataFrame(result["top_bearish"]), use_container_width=True)

                    bah = result.get("bah_metrics", {})
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("B&H Total Return", f"{bah.get('total_return_pct',0):+.1f}%")
                    col2.metric("B&H CAGR", f"{bah.get('cagr_pct',0):+.1f}%")
                    col3.metric("Sharpe Ratio", f"{bah.get('sharpe_ratio',0):.3f}")
                    col4.metric("Max Drawdown", f"{bah.get('max_drawdown_pct',0):.1f}%")

            except Exception as e:
                st.error(f"Backtest error: {e}")
                import traceback
                st.code(traceback.format_exc())

# ── Tab 6: Seasonal ────────────────────────────────────────────────────────
with tab6:
    st.subheader("🌞 Seasonal Analysis — Gann's Annual Clock")
    year_input = st.number_input("Year", min_value=2020, max_value=2030,
                                  value=datetime.now().year)
    if st.button("Show Seasonal Dates"):
        try:
            from core.seasonal import get_seasonal_dates, find_next_ingresses
            import pandas as pd
            seasonal = get_seasonal_dates(int(year_input))
            rows = [{"Event": k, "Date": v["date"], "Sign": v["sign"],
                     "Symbol": v["symbol"], "Market Note": v["market"]}
                    for k, v in seasonal.items()]
            st.dataframe(pd.DataFrame(rows), use_container_width=True)

            upcoming = find_next_ingresses(date_str, months_ahead=6)
            if upcoming:
                st.subheader(f"Upcoming Ingresses (from {date_str})")
                updf = pd.DataFrame(upcoming)
                st.dataframe(updf, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
