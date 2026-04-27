"""
============================================================
 Gann Astro Projector — Master Signal Aggregator
============================================================
 Collects signals from all Gann/Western modules, weights them,
 and produces a single daily projection with confidence score.
"""

import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_full_projection(date_str, symbol="nifty", dataset=None):
    """
    Master projection function. Aggregates ALL signal sources.
    Returns a rich dict with final bias, confidence, and per-module signals.
    """
    print(f"\n{'='*65}")
    print(f"  🔮 GANN ASTRO PROJECTION — {symbol.upper()} | {date_str}")
    print(f"{'='*65}")

    signals = []   # (name, direction, weight, detail)
    warnings = []

    # ── 1. Planetary Positions + Dignity ──────────────────────────────────
    try:
        from core.astro_engine import full_astro_analysis
        analysis = full_astro_analysis(date_str)
        pos = analysis["positions"]

        dcomp = analysis["dignity_composite"]
        ebias = analysis["element_bias"]
        retros = analysis["retrogrades"]

        print(f"\n🪐 PLANETARY POSITIONS (Tropical / Western):")
        print(f"{'Planet':10s} {'Sign':14s} {'Deg':>7s} {'Dignity':12s} {'Retro':6s}")
        print("-" * 53)
        for name, d in pos.items():
            r = "℞" if d["retrograde"] else ""
            print(f"{name:10s} {d['sign']:14s} {d['sign_degree']:6.2f}°  {d['dignity']:12s} {r}")

        if dcomp >= 10:
            signals.append(("Dignity Composite HIGH", "BULLISH", 15,
                            f"Overall planetary strength score: +{dcomp}"))
        elif dcomp <= -5:
            signals.append(("Dignity Composite LOW", "BEARISH", 15,
                            f"Overall planetary weakness score: {dcomp}"))

        if ebias == "BULLISH":
            signals.append(("Fire/Air Element Dominance", "BULLISH", 10,
                            "Fire+Air planets dominant → expansive energy"))
        elif ebias == "BEARISH":
            signals.append(("Earth/Water Element Dominance", "BEARISH", 10,
                            "Earth+Water planets dominant → contractive energy"))

        if len(retros) >= 3:
            warnings.append(f"⚠️  {len(retros)} planets retrograde: {', '.join(retros)}")
            signals.append(("Multiple Retrogrades", "BEARISH", 12,
                            f"{', '.join(retros)} all retrograde → caution"))
        elif len(retros) == 0:
            signals.append(("No Retrogrades", "BULLISH", 8,
                            "All planets direct → smooth energy flow"))

    except Exception as e:
        print(f"   ⚠️  Planetary engine error: {e}")

    # ── 2. Planetary Aspects ───────────────────────────────────────────────
    try:
        from core.aspects import detect_aspects, get_aspect_score
        aspects = detect_aspects(pos)
        ascore  = get_aspect_score(aspects)

        print(f"\n🔗 MAJOR ASPECTS TODAY:")
        for a in aspects[:6]:
            tight = " [TIGHT]" if a["tight"] else ""
            print(f"   {a['planet1']:10s} ☌ {a['planet2']:10s}  "
                  f"{a['aspect']:14s}  {a['market_signal']:20s}{tight}")

        asp_bias = ascore["bias"]
        asp_weight = min(ascore["total"] // 5, 20)
        signals.append((f"Aspect Score ({asp_bias})", asp_bias, asp_weight,
                        f"Bull:{ascore['bullish']} Bear:{ascore['bearish']} Vol:{ascore['volatile']}"))

        # Extra weight for tight aspects
        tight_aspects = [a for a in aspects if a["tight"]]
        for ta in tight_aspects[:2]:
            if "BULLISH" in ta["market_signal"] or "TRINE" in ta["aspect"]:
                signals.append((f"TIGHT {ta['aspect']}: {ta['planet1']}-{ta['planet2']}",
                                "BULLISH", 8, "Tight harmonious aspect"))
            elif "TURNING" in ta["market_signal"] or ta["aspect"] in ["Square","Opposition"]:
                signals.append((f"TIGHT {ta['aspect']}: {ta['planet1']}-{ta['planet2']}",
                                "VOLATILE", 8, "Tight stress aspect → turning point"))

    except Exception as e:
        print(f"   ⚠️  Aspect engine error: {e}")

    # ── 3. Retrograde Analysis ─────────────────────────────────────────────
    try:
        from core.retrograde import retrograde_market_score
        rscore = retrograde_market_score(date_str)
        if rscore["count"] > 0:
            print(f"\n℞ RETROGRADE PLANETS: {', '.join(rscore['retrograde_planets'])}")
            print(f"   Signal: {rscore['market_signal']}")
            if "BEARISH" in rscore["market_signal"]:
                signals.append(("Retrograde Stack", "BEARISH",
                                min(rscore["total_weight"], 18), rscore["market_signal"]))

    except Exception as e:
        print(f"   ⚠️  Retrograde engine error: {e}")

    # ── 4. Seasonal / Cardinal Ingresses ──────────────────────────────────
    try:
        from core.seasonal import find_next_ingresses, days_to_next_cardinal
        upcoming = find_next_ingresses(date_str, months_ahead=1)
        next_card = days_to_next_cardinal(date_str)

        if upcoming:
            print(f"\n🌞 UPCOMING SOLAR INGRESSES (30 days):")
            for evt in upcoming[:4]:
                card_flag = " ⭐ CARDINAL" if evt["is_cardinal"] else ""
                print(f"   {evt['date']}  {evt['event']:40s}{card_flag}")
                if evt["is_cardinal"] and evt["days_away"] <= 5:
                    signals.append((f"Cardinal Ingress Near: {evt['sign']}",
                                    "VOLATILE", 15,
                                    f"{evt['event']} in {evt['days_away']} days"))
                elif evt["is_cardinal"] and evt["days_away"] <= 14:
                    signals.append((f"Cardinal Ingress Approaching: {evt['sign']}",
                                    "VOLATILE", 8,
                                    f"{evt['event']} in {evt['days_away']} days"))

    except Exception as e:
        print(f"   ⚠️  Seasonal engine error: {e}")

    # ── 5. Sector Rotation ─────────────────────────────────────────────────
    try:
        from core.sector_map import get_top_sectors
        sector_result = get_top_sectors(pos)
        print(f"\n🏭 SECTOR SIGNALS:")
        print(f"   BULLISH sectors:")
        for s in sector_result["bullish_sectors"][:3]:
            print(f"     {s['planet']:10s} ({s['dignity']:10s}) → {', '.join(s['sectors'][:2])}")
        print(f"   BEARISH sectors:")
        for s in sector_result["bearish_sectors"][:3]:
            print(f"     {s['planet']:10s} ({s['dignity']:10s}) → {', '.join(s['sectors'][:2])}")
    except Exception as e:
        print(f"   ⚠️  Sector engine error: {e}")

    # ── 6. Gann Square of Nine Price Levels ───────────────────────────────
    try:
        from analysis.gann_levels import gann_sq9_levels
        from market.data_fetcher import get_latest_price
        price, _ = get_latest_price(symbol)
        if price:
            sq9 = gann_sq9_levels(price)
            print(f"\n📐 GANN SQUARE OF NINE for {symbol.upper()} @ {price:.2f}:")
            print(f"   Resistance: {[r['price'] for r in sq9['resistance'][:4]]}")
            print(f"   Support:    {[s['price'] for s in sq9['support'][:4]]}")
    except Exception:
        pass

    # ── 7. Aggregate Signals ──────────────────────────────────────────────
    if not signals:
        signals.append(("No clear signal", "NEUTRAL", 5, "Insufficient data"))

    bullish_w = sum(w for _, d, w, _ in signals if d == "BULLISH")
    bearish_w = sum(w for _, d, w, _ in signals if d == "BEARISH")
    volatile_w= sum(w for _, d, w, _ in signals if d == "VOLATILE")
    total_w   = bullish_w + bearish_w + volatile_w or 1

    if bullish_w >= bearish_w and bullish_w >= volatile_w:
        final_bias = "BULLISH"
        confidence = round(bullish_w / total_w * 100, 1)
    elif bearish_w >= bullish_w and bearish_w >= volatile_w:
        final_bias = "BEARISH"
        confidence = round(bearish_w / total_w * 100, 1)
    else:
        final_bias = "VOLATILE / NEUTRAL"
        confidence = round(volatile_w / total_w * 100, 1)

    # Confidence capped at 85% (astrology is probabilistic, not certain)
    confidence = min(confidence, 85.0)

    print(f"\n{'─'*65}")
    print(f"  📊 ALL SIGNALS COLLECTED:")
    for name, direction, weight, detail in signals:
        emoji = "🟢" if direction == "BULLISH" else ("🔴" if direction == "BEARISH" else "🟡")
        print(f"  {emoji} [{weight:2d}] {name}: {detail[:50]}")

    for w in warnings:
        print(f"  {w}")

    print(f"\n{'='*65}")
    print(f"  🎯 FINAL PROJECTION: {final_bias}")
    print(f"  📊 Confidence: {confidence}% (Gann score: Bull={bullish_w} | Bear={bearish_w} | Vol={volatile_w})")
    print(f"  ⚠️  DISCLAIMER: For research only. Not trading advice.")
    print(f"{'='*65}\n")

    return {
        "date": date_str,
        "symbol": symbol,
        "bias": final_bias,
        "confidence": confidence,
        "bullish_score": bullish_w,
        "bearish_score": bearish_w,
        "volatile_score": volatile_w,
        "signals": signals,
        "warnings": warnings,
    }
