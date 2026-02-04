from collections import defaultdict, deque

class MarketState:
    def __init__(self, symbol):
        self.symbol = symbol
        self.last_candle = None
        self.tick_prices = []
        self.last_score = None

    def add_tick(self, price):
        self.tick_prices.append(price)
        if len(self.tick_prices) > 20:
            self.tick_prices.pop(0)

    def set_candle(self, candle):
        self.last_candle = candle
        self.tick_prices.clear()

