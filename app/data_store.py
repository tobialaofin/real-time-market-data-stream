from collections import deque
from typing import Dict, Deque, Tuple
import time

TimeSeries = Deque[Tuple[float, float]]

class MarketDataStore:
    def __init__(self, max_points: int = 600):
        self.max_points = max_points
        self.data: Dict[str, TimeSeries] = {}

    def add_point(self, symbol: str, price: float, ts: float | None = None):
        ts = ts or time.time()
        symbol = symbol.upper()
        if symbol not in self.data:
            self.data[symbol] = deque(maxlen=self.max_points)
        self.data[symbol].append((ts, float(price)))

    def get_series(self, symbol: str) -> TimeSeries:
        return self.data.get(symbol.upper(), deque())

data_store = MarketDataStore()
