import asyncio
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from .processor import get_symbol_snapshot
from .fetcher import simulate_stream, stooq_poll, DEFAULT_SYMBOLS

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
DASHBOARD_DIR = BASE_DIR / "dashboard"

app.mount("/static", StaticFiles(directory=DASHBOARD_DIR / "static"), name="static")

@app.on_event("startup")
async def startup():
    asyncio.create_task(simulate_stream(DEFAULT_SYMBOLS, poll_interval=1.0))

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return FileResponse(DASHBOARD_DIR / "index.html")

@app.get("/api/snapshot")
async def snapshot(symbols: str = "AAPL,MSFT,SPY", window: int = 60):
    syms = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    out = {}
    for s in syms:
        out[s] = get_symbol_snapshot(s, window=window)
    return out

@app.post("/api/mode")
async def set_mode(mode: str = "simulate", symbols: str = "AAPL,MSFT,SPY", poll_interval: float = 5.0):
    syms = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    if mode == "stooq":
        asyncio.create_task(stooq_poll(syms, poll_interval=max(2.0, float(poll_interval))))
        return {"mode": "stooq", "symbols": syms, "poll_interval": max(2.0, float(poll_interval))}
    asyncio.create_task(simulate_stream(syms, poll_interval=max(0.5, float(poll_interval))))
    return {"mode": "simulate", "symbols": syms, "poll_interval": max(0.5, float(poll_interval))}
