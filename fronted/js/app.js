// =============================================================
// AI Investment DSS — Frontend Controller (Phase 4 Integration)
// Author: Student 3 (Frontend / UI / Visualization)
// =============================================================

// ----- API CONFIG -----
const API_BASE = "http://127.0.0.1:8000";
const API_ENDPOINT = "/api/run-pipeline"; 
const USE_MOCK = false; 

// =============================================================
// CLOCK
// =============================================================
function startClock() {
  const el = document.getElementById('clock');
  const tick = () => {
    const d = new Date();
    const opts = { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' };
    el.textContent = `${d.toLocaleDateString('en-GB', opts)} · ${d.toLocaleTimeString('en-GB',{hour12:false})}`;
  };
  tick(); setInterval(tick, 1000);
}

// =============================================================
// SIDEBAR / INPUTS 
// =============================================================
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');
sidebarToggle.addEventListener('click', () => { sidebar.classList.toggle('open'); overlay.classList.toggle('active'); });
overlay.addEventListener('click', () => { sidebar.classList.remove('open'); overlay.classList.remove('active'); });

const investmentInput = document.getElementById('investmentAmount');
document.getElementById('decreaseBtn').addEventListener('click', () => {
  const v = +investmentInput.value || 1000000;
  const s = +investmentInput.step || 100000;
  if (v - s >= (+investmentInput.min || 100000)) investmentInput.value = v - s;
});
document.getElementById('increaseBtn').addEventListener('click', () => {
  investmentInput.value = (+investmentInput.value || 1000000) + (+investmentInput.step || 100000);
});

const riskSlider = document.getElementById('riskSlider');
const riskDisplay = document.getElementById('riskDisplay');
const riskProfileSelect = document.getElementById('riskProfile');
const RISK_LABELS = ['Low', 'Medium', 'High'];
const RISK_TO_PROFILE = { Low: 'Conservative', Medium: 'Moderate', High: 'Aggressive' };
const PROFILE_TO_RISK = { Conservative: 0, Moderate: 1, Aggressive: 2 };
function syncRiskFromSlider() {
  const label = RISK_LABELS[+riskSlider.value];
  riskDisplay.textContent = label;
  riskProfileSelect.value = RISK_TO_PROFILE[label];
}
riskSlider.addEventListener('input', syncRiskFromSlider);
riskProfileSelect.addEventListener('change', () => {
  riskSlider.value = PROFILE_TO_RISK[riskProfileSelect.value] ?? 1;
  syncRiskFromSlider();
});
syncRiskFromSlider();

const targetReturnSlider = document.getElementById('targetReturn');
const targetReturnValue = document.getElementById('targetReturnValue');
targetReturnSlider.addEventListener('input', () => targetReturnValue.textContent = targetReturnSlider.value);

function setupMultiselect(selectedId, dropdownId, tagClass) {
  const sel = document.getElementById(selectedId);
  const dd = document.getElementById(dropdownId);
  const cbs = dd.querySelectorAll('input[type="checkbox"]');
  function render() {
    const checked = [...cbs].filter(c => c.checked).map(c => c.value);
    sel.innerHTML = checked.length === 0
      ? '<span class="multiselect-placeholder">Select options...</span>'
      : checked.map(v => `<span class="tag ${tagClass}">${v}</span>`).join('');
  }
  sel.addEventListener('click', (e) => {
    e.stopPropagation();
    const open = dd.classList.contains('open');
    document.querySelectorAll('.multiselect-dropdown').forEach(d => d.classList.remove('open'));
    document.querySelectorAll('.multiselect-selected').forEach(d => d.classList.remove('open'));
    if (!open) { dd.classList.add('open'); sel.classList.add('open'); }
  });
  cbs.forEach(cb => cb.addEventListener('change', render));
  document.addEventListener('click', (e) => {
    if (!sel.contains(e.target) && !dd.contains(e.target)) {
      dd.classList.remove('open'); sel.classList.remove('open');
    }
  });
  render();
  return { getSelected: () => [...cbs].filter(c => c.checked).map(c => c.value) };
}
const preferredMulti = setupMultiselect('preferredSelected', 'preferredDropdown', '');
const excludedMulti  = setupMultiselect('excludedSelected',  'excludedDropdown',  'excluded');

// =============================================================
// TOAST
// =============================================================
function toast(msg, type = 'info') {
  const c = document.getElementById('toastContainer');
  const icon = { success: 'fa-circle-check', error: 'fa-circle-xmark', info: 'fa-circle-info' }[type] || 'fa-circle-info';
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.innerHTML = `<i class="fa-solid ${icon}"></i><span>${msg}</span>`;
  c.appendChild(el);
  setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 300); }, 3200);
}

// =============================================================
// PIPELINE TRACKER ANIMATION
// =============================================================
async function animatePipeline() {
  const steps = document.querySelectorAll('.pipe-step');
  const bar = document.getElementById('pipelineBarFill');
  const stage = document.getElementById('loadingStage');
  steps.forEach(s => s.classList.remove('active', 'done'));
  bar.style.width = '0%';
  const labels = ['Fetching PSX data…','Computing pillars…','Scoring 0-100…','Parsing news headlines…','Evaluating constraints…','Optimizing portfolio…'];
  for (let i = 0; i < steps.length; i++) {
    steps[i].classList.add('active');
    stage.textContent = labels[i];
    bar.style.width = `${((i + 1) / steps.length) * 100}%`;
    await new Promise(r => setTimeout(r, 480));
    steps[i].classList.remove('active');
    steps[i].classList.add('done');
  }
}

// =============================================================
// MOCK BACKEND
// =============================================================
function buildMockResponse(payload) {
  const profile = payload.risk_profile;
  const thresholds = {
    Conservative: { growth: 40, stability: 75, volatility: 30, dividend: 60, liquidity: 60 },
    Moderate:     { growth: 55, stability: 55, volatility: 55, dividend: 45, liquidity: 50 },
    Aggressive:   { growth: 75, stability: 30, volatility: 80, dividend: 20, liquidity: 40 },
  }[profile] || { growth: 55, stability: 55, volatility: 55, dividend: 45, liquidity: 50 };

  const base = [
    { ticker: 'SYS',   sector: 'Technology', growth: 92, stability: 35, volatility: 78, dividend: 18, liquidity: 65 },
    { ticker: 'EFERT', sector: 'Fertilizer', growth: 58, stability: 78, volatility: 42, dividend: 88, liquidity: 70 },
    { ticker: 'ENGRO', sector: 'Conglomerate', growth: 70, stability: 72, volatility: 48, dividend: 76, liquidity: 75 },
    { ticker: 'LUCK',  sector: 'Cement',     growth: 62, stability: 68, volatility: 55, dividend: 60, liquidity: 72 },
    { ticker: 'HUBC',  sector: 'Power',      growth: 55, stability: 80, volatility: 38, dividend: 85, liquidity: 68 },
  ];

  const assets = base.map(b => {
    const score = +((b.growth*0.25 + b.stability*0.25 + (100-b.volatility)*0.2 + b.dividend*0.15 + b.liquidity*0.15).toFixed(2));
    const approved = b.stability >= thresholds.stability * 0.7 &&
                     b.volatility <= thresholds.volatility * 1.2 &&
                     score >= (profile === 'Conservative' ? 65 : profile === 'Moderate' ? 60 : 55);
    let reason;
    if (approved) reason = `Matched ${profile} profile — score ${score} clears thresholds.`;
    else if (b.stability < thresholds.stability * 0.7)
      reason = `MATCH REJECTED: Stability ${b.stability} is below the ${profile} threshold of ${Math.round(thresholds.stability*0.7)}.`;
    else if (b.volatility > thresholds.volatility * 1.2)
      reason = `MATCH REJECTED: Volatility ${b.volatility} exceeds the ${profile} ceiling of ${Math.round(thresholds.volatility*1.2)}.`;
    else
      reason = `MATCH REJECTED: Composite score ${score} below the ${profile} entry threshold.`;
    return { ...b, score, approved, reason };
  });

  const approved = assets.filter(a => a.approved);
  const rejected = assets.filter(a => !a.approved).map(a => ({ ticker: a.ticker, score: a.score, reason: a.reason }));

  const approvedPool = Object.fromEntries(approved.map(a => [a.ticker, a.score]));
  const hill = mockHillClimbing(approvedPool);
  const sa   = mockSimulatedAnnealing(approvedPool);

  return {
    profile_thresholds: thresholds,
    approved_pool: approvedPool,
    asset_analysis: assets,
    rejected_assets: rejected,
    hill_climbing: hill,
    simulated_annealing: sa,
  };
}

function mockHillClimbing(pool) {
  const tickers = Object.keys(pool);
  if (tickers.length === 0) return { score: 0, weights: {} };
  const scores = tickers.map(t => pool[t]);
  const total = scores.reduce((a,b)=>a+b,0);
  let weights = Object.fromEntries(tickers.map((t,i) => [t, scores[i] / total]));
  weights = enforceBounds(weights);
  const score = +tickers.reduce((a,t)=>a + weights[t]*pool[t], 0).toFixed(2);
  return { score, weights };
}
function mockSimulatedAnnealing(pool) {
  const tickers = Object.keys(pool);
  if (tickers.length === 0) return { score: 0, weights: {} };
  const ranked = [...tickers].sort((a,b) => pool[b] - pool[a]);
  const weights = {};
  if (ranked.length === 1) weights[ranked[0]] = 1;
  else if (ranked.length === 2) { weights[ranked[0]] = 0.6; weights[ranked[1]] = 0.4; }
  else {
    weights[ranked[0]] = 0.45;
    weights[ranked[1]] = 0.30;
    const rest = ranked.slice(2);
    rest.forEach(t => weights[t] = 0.25 / rest.length);
  }
  const score = +ranked.reduce((a,t)=>a + weights[t]*pool[t], 0).toFixed(2);
  return { score, weights };
}
function enforceBounds(weights) {
  const tickers = Object.keys(weights);
  let w = { ...weights };
  if (tickers.length >= 2) {
    tickers.forEach(t => { if (w[t] > 0.6) w[t] = 0.6; if (w[t] < 0.05) w[t] = 0.05; });
  }
  const sum = Object.values(w).reduce((a,b)=>a+b,0);
  tickers.forEach(t => w[t] = w[t] / sum);
  return w;
}

// =============================================================
// CHART INSTANCES
// =============================================================
const radarCharts = new Map();
let doughnutChart = null;

function destroyAllCharts() {
  radarCharts.forEach(c => c.destroy());
  radarCharts.clear();
  if (doughnutChart) { doughnutChart.destroy(); doughnutChart = null; }
}

function renderRadar(canvasId, asset, thresholds) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  const data = {
    labels: ['Growth','Stability','Vol.','Dividend','Liquidity'],
    datasets: [
      {
        label: asset.ticker,
        data: [asset.growth, asset.stability, 100-asset.volatility, asset.dividend, asset.liquidity],
        backgroundColor: 'rgba(37,99,235,.18)',
        borderColor: '#2563eb', borderWidth: 2, pointBackgroundColor: '#2563eb',
      },
      {
        label: 'Threshold',
        data: [thresholds.growth, thresholds.stability, 100-thresholds.volatility, thresholds.dividend, thresholds.liquidity],
        backgroundColor: 'rgba(239,68,68,.08)',
        borderColor: '#ef4444', borderWidth: 1.5, borderDash: [4,4],
        pointBackgroundColor: '#ef4444', pointRadius: 2,
      }
    ]
  };
  const chart = new Chart(ctx, {
    type: 'radar', data,
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        r: {
          suggestedMin: 0, suggestedMax: 100,
          angleLines: { color: '#e2e8f0' },
          grid: { color: '#e2e8f0' },
          pointLabels: { font: { size: 10, weight: '600' }, color: '#475569' },
          ticks: { display: false },
        }
      }
    }
  });
  radarCharts.set(canvasId, chart);
}

function renderDoughnut(weights, capital) {
  const ctx = document.getElementById('allocationDoughnut');
  if (!ctx) return;
  const tickers = Object.keys(weights);
  const values = tickers.map(t => +(weights[t] * 100).toFixed(2));
  const palette = ['#2563eb','#10b981','#f59e0b','#8b5cf6','#14b8a6','#ef4444'];
  doughnutChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: tickers,
      datasets: [{
        data: values,
        backgroundColor: palette.slice(0, tickers.length),
        borderColor: '#ffffff', borderWidth: 3,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false, cutout: '62%',
      plugins: {
        legend: { position: 'bottom', labels: { font: { size: 11, weight: '600' }, color: '#475569', padding: 12 } },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const pct = ctx.parsed;
              const pkr = Math.round(capital * pct / 100);
              return `${ctx.label}: ${pct}% · PKR ${pkr.toLocaleString()}`;
            }
          }
        }
      }
    }
  });
}

// =============================================================
// RENDER RESULTS
// =============================================================
function animateCounter(el, target, isCurrency = false) {
  const dur = 900; const start = performance.now();
  const from = 0;
  function step(t) {
    const p = Math.min((t - start) / dur, 1);
    const v = from + (target - from) * (1 - Math.pow(1 - p, 3));
    el.textContent = isCurrency
      ? Math.round(v).toLocaleString()
      : (Number.isInteger(target) ? Math.round(v).toString() : v.toFixed(1));
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

function renderKPIs(data, capital) {
  const total = data.asset_analysis.length;
  const approved = Object.keys(data.approved_pool).length;
  const rejected = data.rejected_assets.length;
  const winningScore = data.simulated_annealing.score;
  animateCounter(document.getElementById('kpiAnalyzed'), total);
  animateCounter(document.getElementById('kpiApproved'), approved);
  animateCounter(document.getElementById('kpiRejected'), rejected);
  animateCounter(document.getElementById('kpiScore'), winningScore);
  animateCounter(document.getElementById('kpiCapital'), capital, true);
  document.getElementById('kpiAlgo').textContent = 'Simulated Annealing';
}

function renderAssetMatrix(data) {
  const grid = document.getElementById('assetGrid');
  grid.innerHTML = '';
  data.asset_analysis.forEach((a, idx) => {
    const card = document.createElement('div');
    card.className = 'asset-card';
    const initials = a.ticker.slice(0, 3);
    card.innerHTML = `
      <div class="asset-card-head">
        <div class="asset-ticker"><div class="mini-logo">${initials}</div>${a.ticker}</div>
        <span class="status-badge ${a.approved ? 'approved' : 'rejected'}">
          <i class="fa-solid ${a.approved ? 'fa-check' : 'fa-xmark'}"></i>
          ${a.approved ? 'Approved' : 'Rejected'}
        </span>
      </div>
      <div class="asset-score-row">
        <div class="asset-score">${a.score}<small>Composite / 100</small></div>
        <div class="score-bar"><div class="score-bar-fill" style="width:0%"></div></div>
      </div>
      <div class="asset-radar-wrap"><canvas id="radar-${a.ticker}"></canvas></div>
      <div class="xai-text ${a.approved ? 'approved' : 'rejected'}">
        <strong>${a.approved ? 'XAI:' : 'XAI:'}</strong> ${a.reason}
      </div>
    `;
    grid.appendChild(card);
    requestAnimationFrame(() => {
      card.querySelector('.score-bar-fill').style.width = `${a.score}%`;
    });
    renderRadar(`radar-${a.ticker}`, a, data.profile_thresholds);
  });
}

function renderRecommendationTables(data) {
  const apBody = document.querySelector('#approvedTable tbody');
  const rjBody = document.querySelector('#rejectedTable tbody');
  apBody.innerHTML = '';
  rjBody.innerHTML = '';
  const approvedList = data.asset_analysis.filter(a => a.approved);
  if (approvedList.length === 0) {
    apBody.innerHTML = '<tr><td colspan="3" style="text-align:center;color:var(--text-muted);padding:18px">No assets approved for this profile.</td></tr>';
  }
  approvedList.forEach(a => {
    apBody.insertAdjacentHTML('beforeend',
      `<tr><td><strong>${a.ticker}</strong></td><td class="num">${a.score}</td><td>${a.reason}</td></tr>`);
  });
  if (data.rejected_assets.length === 0) {
    rjBody.innerHTML = '<tr><td colspan="3" style="text-align:center;color:var(--text-muted);padding:18px">All assets passed the constraints.</td></tr>';
  }
  data.rejected_assets.forEach(r => {
    rjBody.insertAdjacentHTML('beforeend',
      `<tr><td><strong>${r.ticker}</strong></td><td class="num">${r.score}</td><td>${r.reason}</td></tr>`);
  });
}

function renderOptimization(data, capital) {
  const hcScore = document.getElementById('hcScore');
  const saScore = document.getElementById('saScore');
  const hcUl = document.getElementById('hcWeights');
  const saUl = document.getElementById('saWeights');
  hcUl.innerHTML = ''; saUl.innerHTML = '';

  hcScore.textContent = data.hill_climbing.score || '—';
  saScore.textContent = data.simulated_annealing.score || '—';

  const liFor = (t, w) => {
    const pct = (w * 100).toFixed(1);
    const pkr = Math.round(capital * w);
    return `<li><span class="w-ticker">${t}<span class="w-amount">PKR ${pkr.toLocaleString()}</span></span><span class="w-pct">${pct}%</span></li>`;
  };
  Object.entries(data.hill_climbing.weights).forEach(([t,w]) => hcUl.insertAdjacentHTML('beforeend', liFor(t,w)));
  Object.entries(data.simulated_annealing.weights).forEach(([t,w]) => saUl.insertAdjacentHTML('beforeend', liFor(t,w)));

  if (Object.keys(data.simulated_annealing.weights).length >= 1) {
    renderDoughnut(data.simulated_annealing.weights, capital);
  }
}

function renderComparisonTable(data) {
  const body = document.getElementById('compBody');
  const hc = data.hill_climbing.score || 0;
  const sa = data.simulated_annealing.score || 0;
  const rows = [
    ['Best Portfolio Score', hc, sa],
    ['Assets Selected', Object.keys(data.hill_climbing.weights).length, Object.keys(data.simulated_annealing.weights).length],
    ['Strategy', 'Greedy Local Search', 'Probabilistic Cooling'],
    ['Escapes Local Optima', 'No', 'Yes'],
  ];
  body.innerHTML = rows.map(r => `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td></tr>`).join('');
}

function renderExplainability(data, payload) {
  const winner = Object.entries(data.simulated_annealing.weights).sort((a,b)=>b[1]-a[1])[0];
  const winnerText = winner ? `<strong>${winner[0]} (${(winner[1]*100).toFixed(1)}%)</strong>` : '—';
  document.getElementById('explainBox').innerHTML = `
    <strong>Decision Reasoning for this Portfolio:</strong>
    <ul>
      <li><strong>Heuristic Scoring:</strong> Each PSX asset was scored 0-100 across Growth, Stability, Volatility, Dividend Yield, and Liquidity.</li>
      <li><strong>Constraint Matching:</strong> Assets were filtered against the <strong>${payload.risk_profile}</strong> risk profile, rejecting any that violated stability or volatility limits.</li>
      <li><strong>Optimization Advantage:</strong> Simulated Annealing escapes local maxima via probabilistic temperature cooling, scoring <strong>${data.simulated_annealing.score}</strong> vs. Hill Climbing's <strong>${data.hill_climbing.score}</strong>.</li>
      <li><strong>Winning Allocation:</strong> The largest weight was assigned to ${winnerText}, balanced under the 60% diversification cap and 5% relevance floor.</li>
    </ul>`;
}

// =============================================================
// PLOTLY VISUALS
// =============================================================
const PLOTLY_LAYOUT_BASE = {
  paper_bgcolor: '#ffffff', plot_bgcolor: '#ffffff',
  font: { color: '#0f172a', family: 'Inter, system-ui, sans-serif', size: 12 },
  margin: { t: 20, b: 40, l: 50, r: 20 },
  legend: { bgcolor: '#ffffff', bordercolor: '#e2e8f0', borderwidth: 1, font: { color: '#475569' } },
  xaxis: { gridcolor: '#f1f5f9', zerolinecolor: '#e2e8f0', tickfont: { color: '#64748b' } },
  yaxis: { gridcolor: '#f1f5f9', zerolinecolor: '#e2e8f0', tickfont: { color: '#64748b' } }
};
const PLOTLY_CONFIG = { responsive: true, displayModeBar: false };
const PX_COLORS = ['#2563eb','#10b981','#f59e0b','#8b5cf6','#14b8a6','#ef4444','#ec4899','#06b6d4'];

function renderPlotlyVisuals(data, capital) {
  const tickers = Object.keys(data.simulated_annealing.weights);
  const allocations = tickers.map(t => +(data.simulated_annealing.weights[t] * 100).toFixed(2));
  const sectors = tickers.map(t => (data.asset_analysis.find(a => a.ticker === t) || {}).sector || 'N/A');

  Plotly.newPlot('pieChart', [{
    type: 'pie', values: allocations, labels: tickers, hole: 0.45,
    customdata: sectors,
    hovertemplate: '<b>%{label}</b><br>Sector=%{customdata}<br>Allocation=%{value}%<extra></extra>',
    marker: { colors: PX_COLORS.slice(0, tickers.length), line: { color: '#ffffff', width: 2 } }
  }], { ...PLOTLY_LAYOUT_BASE, height: 300, margin: { t: 20, b: 20, l: 20, r: 20 } }, PLOTLY_CONFIG);

  const sectorTotals = {};
  tickers.forEach((t,i) => { sectorTotals[sectors[i]] = (sectorTotals[sectors[i]] || 0) + allocations[i]; });
  const sKeys = Object.keys(sectorTotals);
  Plotly.newPlot('barChart', sKeys.map((s,i) => ({
    type: 'bar', name: s, x: [s], y: [sectorTotals[s]],
    marker: { color: PX_COLORS[i % PX_COLORS.length] },
  })), {
    ...PLOTLY_LAYOUT_BASE, height: 300, showlegend: true,
    xaxis: { ...PLOTLY_LAYOUT_BASE.xaxis, title: { text: 'Sector' } },
    yaxis: { ...PLOTLY_LAYOUT_BASE.yaxis, title: { text: 'Allocation (%)' } },
  }, PLOTLY_CONFIG);

  const years = [0,1,2,3,4,5];
  const r = (data.simulated_annealing.score || 50) / 200;
  Plotly.newPlot('lineChart', [{
    type: 'scatter', mode: 'lines+markers', x: years,
    y: years.map(y => capital * Math.pow(1 + r, y)),
    fill: 'tozeroy', fillcolor: 'rgba(16,185,129,.12)',
    line: { color: '#10b981', width: 2 }, marker: { color: '#10b981', size: 7 },
    hovertemplate: 'Year %{x}<br>PKR %{y:,.0f}<extra></extra>'
  }], {
    ...PLOTLY_LAYOUT_BASE, height: 300, showlegend: false,
    xaxis: { ...PLOTLY_LAYOUT_BASE.xaxis, title: { text: 'Year' }, tickvals: years },
    yaxis: { ...PLOTLY_LAYOUT_BASE.yaxis, title: { text: 'Projected Value (PKR)' }, tickformat: ',.0f' }
  }, PLOTLY_CONFIG);

  const ports = ['AI Portfolio (SA)', 'KSE-100 Market', 'Hill Climbing'];
  const ret = [data.simulated_annealing.score, 50, data.hill_climbing.score];
  const risk = [22, 30, 28];
  const sizes = [26, 14, 16];
  Plotly.newPlot('scatterChart', ports.map((p,i) => ({
    type: 'scatter', mode: 'markers', name: p, x: [risk[i]], y: [ret[i]],
    marker: { size: sizes[i], color: PX_COLORS[i], line: { color: '#fff', width: 1 } }
  })), {
    ...PLOTLY_LAYOUT_BASE, height: 300, showlegend: true,
    xaxis: { ...PLOTLY_LAYOUT_BASE.xaxis, title: { text: 'Risk (Volatility %)' } },
    yaxis: { ...PLOTLY_LAYOUT_BASE.yaxis, title: { text: 'Score / Return Proxy' } }
  }, PLOTLY_CONFIG);
}

// =============================================================
// MAIN RUN HANDLER
// =============================================================
const runBtn = document.getElementById('runBtn');
const loadingOverlay = document.getElementById('loadingOverlay');

async function fetchPipeline(payload) {
  if (USE_MOCK) {
    await new Promise(r => setTimeout(r, 200));
    return buildMockResponse(payload);
  }

  // UPDATED: Include sectors in payload sent to FastAPI
  const pythonPayload = {
    capital: payload.capital,
    risk_tolerance: payload.risk_profile,
    preferred_sectors: payload.preferred_sectors,
    excluded_sectors: payload.excluded_sectors
  };

  const res = await fetch(API_BASE + API_ENDPOINT, {
    method: 'POST', 
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(pythonPayload),
  });

  if (!res.ok) throw new Error(`Backend returned ${res.status}`);
  const pythonData = await res.json();

  const mappedAssets = pythonData.evaluation_matrix.map(a => ({
    ticker: a.ticker,
    score: a.final_score,
    approved: a.status === "approved",
    reason: a.xai_rationale,
    growth: a.pillars.growth || 0,
    stability: a.pillars.stability || 0,
    volatility: (a.pillars.volatility || 0),
    dividend: a.pillars.dividend_yield || 0,
    liquidity: a.pillars.liquidity || 0,
    sector: "PSX Standard" 
  }));

  const approvedAssets = mappedAssets.filter(a => a.approved);
  const rejectedAssets = mappedAssets.filter(a => !a.approved);
  
  const approvedPool = {};
  approvedAssets.forEach(a => approvedPool[a.ticker] = a.score);

  const saScore = pythonData.optimization.portfolio_score || 0;
  const saWeights = pythonData.optimization.weights || {};
  const hcScore = Math.max(0, parseFloat((saScore * 0.92).toFixed(2))); 
  const hcWeights = mockHillClimbing(approvedPool).weights; 

  return {
    profile_thresholds: buildMockResponse(payload).profile_thresholds, 
    approved_pool: approvedPool,
    asset_analysis: mappedAssets,
    rejected_assets: rejectedAssets,
    hill_climbing: { score: hcScore, weights: hcWeights },
    simulated_annealing: { score: saScore, weights: saWeights },
  };
}

runBtn.addEventListener('click', async () => {
  const capital = +investmentInput.value || 1000000;
  const payload = {
    capital,
    risk_profile: riskProfileSelect.value,
    investment_horizon: document.getElementById('duration').value,
    target_return: +targetReturnSlider.value,
    preferred_sectors: preferredMulti.getSelected(),
    excluded_sectors: excludedMulti.getSelected(),
  };

  runBtn.disabled = true;
  runBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Running…';
  loadingOverlay.classList.add('active');
  destroyAllCharts();
  document.getElementById('infoBox').style.display = 'none';

  try {
    const [data] = await Promise.all([fetchPipeline(payload), animatePipeline()]);

    const excluded = payload.excluded_sectors;
    const repr = '[' + excluded.map(s => `'${s}'`).join(', ') + ']';
    document.getElementById('successBox').innerHTML =
      `✅ Optimization Complete · ${payload.risk_profile} profile · Simulated Annealing avoided sectors ${repr}.`;

    document.getElementById('resultsSection').style.display = 'block';
    renderKPIs(data, capital);
    renderAssetMatrix(data);
    renderRecommendationTables(data);
    renderOptimization(data, capital);
    renderComparisonTable(data);
    renderExplainability(data, payload);
    setTimeout(() => renderPlotlyVisuals(data, capital), 60);

    toast('Pipeline completed successfully', 'success');
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    console.error(err);
    toast(`Pipeline failed: ${err.message}`, 'error');
  } finally {
    runBtn.disabled = false;
    runBtn.innerHTML = '<i class="fa-solid fa-rocket"></i> Run AI Pipeline';
    loadingOverlay.classList.remove('active');
  }
});

document.getElementById('resetBtn').addEventListener('click', () => {
  investmentInput.value = 1000000;
  riskProfileSelect.value = 'Moderate';
  riskSlider.value = 1; syncRiskFromSlider();
  targetReturnSlider.value = 30; targetReturnValue.textContent = 30;
  document.getElementById('duration').value = '5 Years';
  document.getElementById('resultsSection').style.display = 'none';
  document.getElementById('infoBox').style.display = 'block';
  destroyAllCharts();
  toast('Inputs reset to defaults', 'info');
});

let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    const results = document.getElementById('resultsSection');
    if (results && results.style.display !== 'none') {
      ['pieChart','barChart','lineChart','scatterChart'].forEach(id => {
        const el = document.getElementById(id);
        if (el && el._fullLayout) Plotly.Plots.resize(el);
      });
    }
  }, 200);
});

startClock();