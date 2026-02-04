from collections import defaultdict, deque

_candles = defaultdict(lambda: deque(maxlen=200))

def store_candle(symbol, candle):
    _candles[symbol].append(candle)

def get_candles(symbol, limit=100):
    return list(_candles[symbol])[-limit:]
