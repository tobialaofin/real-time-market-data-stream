function qs(id) {
  return document.getElementById(id);
}

function toFixedOrDash(x, n = 2) {
  if (x === null || x === undefined) return "—";
  if (Number.isNaN(x)) return "—";
  return Number(x).toFixed(n);
}

function buildSparkline(points, width = 280, height = 70) {
  if (!points || points.length < 2) return "";
  const prices = points.map(p => p[1]);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const span = max - min || 1;
  const step = width / (prices.length - 1);
  let d = "";
  for (let i = 0; i < prices.length; i++) {
    const x = i * step;
    const y = height - ((prices[i] - min) / span) * height;
    d += (i === 0 ? "M" : "L") + x.toFixed(2) + "," + y.toFixed(2) + " ";
  }
  return `<svg viewBox="0 0 ${width} ${height}" width="100%" height="${height}">
    <path d="${d.trim()}" fill="none" stroke="currentColor" stroke-width="2" />
  </svg>`;
}

async function fetchSnapshot(symbols, window) {
  const res = await fetch(`/api/snapshot?symbols=${encodeURIComponent(symbols)}&window=${encodeURIComponent(window)}`);
  return await res.json();
}

function render(data) {
  const cards = qs("cards");
  cards.innerHTML = "";
  Object.entries(data).forEach(([sym, info]) => {
    const last = info.last_price;
    const chg = info.change_pct;
    const avg = info.avg_price;
    const badgeClass = chg === null || chg === undefined ? "badge" : (chg >= 0 ? "badge pos" : "badge neg");
    const sign = chg === null || chg === undefined ? "" : (chg >= 0 ? "+" : "");
    const chgText = chg === null || chg === undefined ? "—" : `${sign}${toFixedOrDash(chg, 2)}%`;
    const spark = buildSparkline(info.points);

    const el = document.createElement("div");
    el.className = "card";
    el.innerHTML = `
      <div class="row">
        <div class="symbol">${sym}</div>
        <div class="price">${last === null || last === undefined ? "—" : toFixedOrDash(last, 2)}</div>
      </div>
      <div class="meta">
        <div><span class="${badgeClass}">Δ ${chgText}</span></div>
        <div><span class="badge">Avg ${toFixedOrDash(avg, 2)}</span></div>
        <div><span class="badge">Pts ${info.count ?? 0}</span></div>
        <div><span class="badge">Win</span></div>
      </div>
      <div class="spark">${spark}</div>
    `;
    cards.appendChild(el);
  });
}

let timer = null;

async function poll() {
  const symbols = qs("symbols").value || "AAPL,MSFT,SPY";
  const window = qs("window").value || 60;
  try {
    const data = await fetchSnapshot(symbols, window);
    render(data);
  } catch (e) {
  }
}

function start() {
  if (timer) clearInterval(timer);
  timer = setInterval(poll, 2000);
  poll();
}

qs("apply").addEventListener("click", start);
start();
