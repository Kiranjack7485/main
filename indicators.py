import pandas as pd
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator

def compute_indicators(candles):
    if not candles or len(candles) < 60:
        return None

    df = pd.DataFrame(candles)

    df["ema_9"] = EMAIndicator(df["close"], 9).ema_indicator()
    df["ema_21"] = EMAIndicator(df["close"], 21).ema_indicator()
    df["ema_50"] = EMAIndicator(df["close"], 50).ema_indicator()

    df["rsi"] = RSIIndicator(df["close"], 14).rsi()

    macd = MACD(df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    df["vol_avg"] = df["volume"].rolling(20).mean()
    df["volume_spike"] = df["volume"] / df["vol_avg"]

    last = df.iloc[-1]

    return {
        "close": float(last["close"]),
        "ema_9": float(last["ema_9"]),
        "ema_21": float(last["ema_21"]),
        "ema_50": float(last["ema_50"]),
        "rsi": float(last["rsi"]),
        "macd": float(last["macd"]),
        "macd_signal": float(last["macd_signal"]),
        "volume_spike": float(last["volume_spike"]),
    }
