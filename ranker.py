# ranker.py

MIN_SCORE = 6.0
TOP_N = 3


def rank_signals(states: dict):
    """
    states = {
        "ETHUSDT": MarketState,
        "BTCUSDT": MarketState,
        ...
    }
    """

    ranked = []

    for symbol, state in states.items():
        if not state.last_score:
            continue

        score_data = state.last_score

        if score_data["score"] >= MIN_SCORE and score_data["bias"]:
            ranked.append({
                "symbol": symbol,
                "score": score_data["score"],
                "bias": score_data["bias"],
                "reasons": score_data["reasons"]
            })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked[:TOP_N]
