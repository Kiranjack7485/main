def risk_plan(signal):
    price = signal["price"]

    if "BULLISH" in signal["trend"]:
        entry = price
        stop_loss = round(price * 0.985, 2)
        target = round(price * 1.03, 2)
        leverage = "5x"
        reason = "Bullish trend with controlled downside"
    else:
        entry = price
        stop_loss = round(price * 1.015, 2)
        target = round(price * 0.97, 2)
        leverage = "3x"
        reason = "Bearish / uncertain momentum"

    return {
        "entry": entry,
        "stop_loss": stop_loss,
        "target": target,
        "leverage": leverage,
        "reason": reason
    }
