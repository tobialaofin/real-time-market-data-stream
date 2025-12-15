import asyncio
import time
import random
import httpx
from .data_store import data_store

DEFAULT_SYMBOLS = ["AAPL", "MSFT", "SPY", "TSLA", "NVDA"]

def _init_prices(symbols: list[str]) -> dict[str, float]:
    base = 100.0
    out = {}
    for i, s in enumerate(symbols):
        out[s] = base + i * 7.5
    return out

async def simulate_stream(symbols: list[str], poll_interval: float = 1.0):
    prices = _init_prices([s.upper() for s in symbols])
    while True:
        now = time.time()
        for s in symbols:
            sym = s.upper()
            drift = random.uniform(-0.35, 0.35)
            shock = 0.0
            if random.random() < 0.02:
                shock = random.uniform(-2.0, 2.0)
            prices[sym] = max(1.0, prices[sym] + drift + shock)
            data_store.add_point(sym, prices[sym], now)
        await asyncio.sleep(poll_interval)

async def stooq_poll(symbols: list[str], poll_interval: float = 5.0):
    async with httpx.AsyncClient(timeout=10.0) as client:
        while True:
            for s in symbols:
                sym = s.upper()
                url = f"https://stooq.com/q/l/?s={sym.lower()}.us&f=sd2t2ohlcv&h&e=csv"
                try:
                    r = await client.get(url)
                    text = r.text.strip().splitlines()
                    if len(text) >= 2:
                        row = text[1].split(",")
                        close = row[6]
                        if close and close != "N/A":
                            data_store.add_point(sym, float(close), time.time())
                except Exception:
                    pass
            await asyncio.sleep(poll_interval)
