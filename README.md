# Real-Time Market Data Stream Processor

A real-time market data streaming system that ingests live (or simulated) equity prices, computes rolling analytics in memory, and serves a live-updating dashboard.

This project was built to simulate the architecture and engineering challenges of low-latency financial data platforms.

---

## 🚀 Features

- Real-time price ingestion via async background tasks
- In-memory time-series storage using fixed-size ring buffers
- Rolling analytics (moving averages, percent change)
- Live dashboard with sparklines and statistics
- Modular backend architecture using FastAPI

---

## 🧠 Architecture Overview

Data Source → Async Ingestion → In-Memory Store → Rolling Analytics → API → Dashboard

---

## 📊 Dashboard

![Live Dashboard](./docs/dashboard.png)

---

## ▶️ Running Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
py -m uvicorn app.main:app --reload
