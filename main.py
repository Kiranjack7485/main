import json
import asyncio
import websockets
from datetime import datetime, time
from zoneinfo import ZoneInfo

from config import SYMBOLS, MIN_SCORE
from market_data import store_candle, get_candles
from indicators import compute_indicators
from scoring import score_signal
from risk import calculate_risk
from telegram import send_alert

BYBIT_WS = "wss://stream.bybit.com/v5/public/linear"

IST = ZoneInfo("Asia/Kolkata")

def trading_time_allowed():
    now = datetime.now(IST).time()
    return time(17, 30) <= now <= time(23, 30)

async def run():
    async with websockets.connect(BYBIT_WS) as ws:
        print("🟢 Connected to Bybit WebSocket")

        # Subscribe to all symbols
        args = [f"kline.1.{s}" for s in SYMBOLS]
        await ws.send(json.dumps({
            "op": "subscribe",
            "args": args
        }))

        while True:
            msg = json.loads(await ws.recv())

            if "topic" not in msg or "data" not in msg:
                continue

            topic = msg["topic"]
            symbol = topic.split(".")[-1]

            k = msg["data"][0]

            # Only closed candles
            if not k["confirm"]:
                continue

            candle = {
                "open": float(k["open"]),
                "high": float(k["high"]),
                "low": float(k["low"]),
                "close": float(k["close"]),
                "volume": float(k["volume"]),
                "close_time": int(k["timestamp"])
            }

            print(f"🕯 {symbol} closed @ {candle['close']}")

            store_candle(symbol, candle)
            candles = get_candles(symbol)

            indicators = compute_indicators(candles)
            if not indicators:
                continue

            signal = score_signal(symbol, indicators)

            print(
                f"📊 {symbol} | Score: {signal['score']} | Trend: {signal['trend']}"
            )

            # 🔒 STRICT + TIME FILTER
            if (
                signal["score"] >= MIN_SCORE
                and trading_time_allowed()
                and "STRONG" in signal["trend"]
            ):
                risk = calculate_risk(signal)
                await send_alert(signal, risk)

asyncio.run(run())
