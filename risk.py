def calculate_risk(signal):
    price = signal["price"]

    if signal["trend"] == "STRONG BULLISH":
        entry = round(price, 2)
        stop_loss = round(price * 0.992, 2)   # ~0.8% SL
        target = round(price * 1.015, 2)      # ~1.5% TP
        leverage = "5x"
        reason = "Bullish continuation with tight SL for scalping"

    elif signal["trend"] == "STRONG BEARISH":
        entry = round(price, 2)
        stop_loss = round(price * 1.008, 2)
        target = round(price * 0.985, 2)
        leverage = "5x"
        reason = "Bearish continuation with controlled downside risk"

    else:
        return None

    return {
        "entry": entry,
        "stop_loss": stop_loss,
        "target": target,
        "leverage": leverage,
        "reason": reason
    }
