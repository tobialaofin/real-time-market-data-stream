from typing import Dict, Any
from .data_store import data_store

def rolling_avg(prices: list[float], window: int) -> float | None:
    if not prices:
        return None
    w = min(window, len(prices))
    return sum(prices[-w:]) / w

def change_pct(prices: list[float], window: int) -> float | None:
    if not prices:
        return None
    w = min(window, len(prices))
    start = prices[-w]
    end = prices[-1]
    if start == 0:
        return None
    return (end - start) / start * 100.0

def get_symbol_snapshot(symbol: str, window: int = 60) -> Dict[str, Any]:
    series = list(data_store.get_series(symbol))
    if not series:
        return {
            "symbol": symbol.upper(),
            "points": [],
            "last_price": None,
            "avg_price": None,
            "change_pct": None,
            "count": 0
        }
    prices = [p for _, p in series]
    last_price = prices[-1]
    avg_price = rolling_avg(prices, window)
    chg = change_pct(prices, window)
    return {
        "symbol": symbol.upper(),
        "points": series[-300:],
        "last_price": last_price,
        "avg_price": avg_price,
        "change_pct": chg,
        "count": len(series)
    }
