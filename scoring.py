def score_signal(symbol, ind):
    score = 0
    reasons = []

    # 🔥 Trend (non-negotiable)
    if ind["ema_9"] > ind["ema_21"] > ind["ema_50"]:
        trend = "STRONG BULLISH"
        score += 4
        reasons.append("Perfect EMA bullish stack")
    elif ind["ema_9"] < ind["ema_21"] < ind["ema_50"]:
        trend = "STRONG BEARISH"
        score += 4
        reasons.append("Perfect EMA bearish stack")
    else:
        return None  # ❌ No trend → no scalp

    # 🧠 RSI (anti exhaustion)
    if 48 <= ind["rsi"] <= 62:
        score += 2
        reasons.append("RSI healthy zone")
    else:
        return None  # ❌ Avoid reversals

    # ⚡ MACD momentum
    if ind["macd"] > ind["macd_signal"]:
        score += 2
        reasons.append("MACD momentum confirmed")

    # 📊 Volume confirmation
    if ind["volume_spike"] >= 1.8:
        score += 2
        reasons.append("Explosive volume expansion")
    else:
        return None  # ❌ No volume → fake move

    return {
        "symbol": symbol,
        "score": min(score, 10),
        "trend": trend,
        "price": ind["close"],
        "reasons": reasons
    }
