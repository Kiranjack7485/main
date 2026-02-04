import json
import asyncio
import websockets
import time
from datetime import datetime, time as dtime
from zoneinfo import ZoneInfo

from config import (
    SYMBOLS,
    MIN_SCORE,
    ALERT_COOLDOWN,
    TRADE_START_HOUR,
    TRADE_START_MIN,
    TRADE_END_HOUR,
    TRADE_END_MIN
)

from market_data import store_candle, get_candles
from indicators import compute_indicators
from scoring import score_signal
from telegram import send_alert

BINANCE_WS = "wss://stream.binance.com:9443/stream?streams="
streams = "/".join([f"{s.lower()}@kline_1m" for s in SYMBOLS])

last_alert_time = {}
IST = ZoneInfo("Asia/Kolkata")


def is_within_trading_window():
    now = datetime.now(IST).time()

    start = dtime(TRADE_START_HOUR, TRADE_START_MIN)
    end = dtime(TRADE_END_HOUR, TRADE_END_MIN)

    return start <= now <= end


def risk_engine(signal):
    entry = signal["price"]
    sl = round(entry * 0.997, 4)
    tp = round(entry * 1.006, 4)

    return {
        "entry": entry,
        "stop_loss": sl,
        "target": tp,
        "leverage": "5x–8x",
        "reason": "US session liquidity + strong momentum + volume confirmation"
    }


async def run():
    async with websockets.connect(BINANCE_WS + streams) as ws:
        print("🟢 Connected to Binance WebSocket")

        while True:
            msg = json.loads(await ws.recv())
            k = msg["data"]["k"]

            if not k["x"]:
                continue

            symbol = k["s"]
            now_ts = time.time()

            candle = {
                "open": float(k["o"]),
                "high": float(k["h"]),
                "low": float(k["l"]),
                "close": float(k["c"]),
                "volume": float(k["v"]),
                "close_time": k["T"]
            }

            store_candle(symbol, candle)
            candles = get_candles(symbol)

            ind = compute_indicators(candles)
            if not ind:
                continue

            signal = score_signal(symbol, ind)
            if not signal or signal["score"] < MIN_SCORE:
                continue

            # ⏰ TIME FILTER (IMPORTANT)
            if not is_within_trading_window():
                print(f"⏳ Signal ignored (outside IST window): {symbol}")
                continue

            # ⛔ Cooldown check
            if symbol in last_alert_time:
                if now_ts - last_alert_time[symbol] < ALERT_COOLDOWN * 60:
                    continue

            risk = risk_engine(signal)
            send_alert(signal, risk)

            last_alert_time[symbol] = now_ts
            print(f"🚨 ALERT SENT → {symbol} | Score {signal['score']}")


asyncio.run(run())
