from state import MarketState
from config import SYMBOLS

SYMBOL_STATES = {
    symbol: MarketState(symbol)
    for symbol in SYMBOLS
}
