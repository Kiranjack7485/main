print("✅ risk.py loaded – version 2026-02-06-01")
def calculate_risk(signal):
    price = float(signal["price"])
    trend = signal.get("trend", "")

    if trend == "STRONG BULLISH":
        return {
            "entry": round(price, 2),
            "stop_loss": round(price * 0.992, 2),
            "target": round(price * 1.015, 2),
            "leverage": "5x",
            "reason": "Bullish momentum scalping setup"
        }

    if trend == "STRONG BEARISH":
        return {
            "entry": round(price, 2),
            "stop_loss": round(price * 1.008, 2),
            "target": round(price * 0.985, 2),
            "leverage": "5x",
            "reason": "Bearish momentum scalping setup"
        }

    return None
