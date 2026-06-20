AI Portfolio Optimizer — v2 (Audited & Corrected)
==================================================
A 100%-parity HTML/CSS/JS conversion of the Streamlit AI Portfolio Optimizer.

SETUP
-----
1. Extract the folder.
2. Open index.html in any modern browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+).
3. No server, no build step, no dependencies to install.
   Plotly.js is loaded from CDN — internet required on first load.

PROJECT STRUCTURE
-----------------
AI-Portfolio-Optimizer/
├── index.html          Main application (audited and corrected)
├── css/
│   └── style.css       Dark theme styles
├── js/
│   └── app.js          All interactivity and chart logic
└── README.txt          This file

AUDIT FIXES IN v2
-----------------
1. SUCCESS MESSAGE FORMAT
   - BEFORE: "avoided the [Technology] sector(s)." (missing quotes)
   - AFTER:  "avoided the ['Technology'] sector(s)."
   - Matches Python list repr exactly: f"{excluded_sectors}" → ['Technology']

2. ALL METRICS ARE STATIC
   - BEFORE: metricReturn was dynamically recalculated from risk/target inputs
   - AFTER:  All 4 metrics are hardcoded (31.2%, 14.5%, 8.4%, Simulated Annealing)
   - Matches original: all 4 st.metric() calls use hardcoded string values

3. METRIC 4 HAS NO DELTA
   - BEFORE: delta div was rendered for all 4 metrics
   - AFTER:  Metric 4 ("Optimization Method") has no delta element
   - Matches original: m4.metric(label=..., value=...) — no delta argument

4. BAR CHART — MATCHES px.bar(color="Sector")
   - BEFORE: Single trace with manual colors array, text labels on bars, no legend
   - AFTER:  One trace per sector (matches px.bar color="Sector" behavior),
             Plotly default color sequence, legend shown, NO text labels on bars

5. EXPLAINABILITY LINE 2 IS HARDCODED
   - BEFORE: "Extra weight was given to the [Banking and Fertilizer] sectors"
             dynamically used preferredSectors from input
   - AFTER:  "Extra weight was given to the Banking and Fertilizer sectors"
             hardcoded exactly as in original Streamlit code

6. DOUBLE CHEVRON BUG FIXED
   - BEFORE: CSS ::after + JS-injected <span> both showed chevrons simultaneously
   - AFTER:  Only CSS ::after on .multiselect-selected provides the chevron,
             JS renders tags only (no chevron span injected)

FEATURES
--------
- Sidebar Investor Profile
- Investment Amount number input (min=100000, step=100000, default=5000000)
- Investment Duration selectbox (1/3/5 Year, default 5 Years)
- Risk Appetite select-slider (Low/Medium/High, default Medium)
- Target Return slider (10–50, default 30)
- Preferred Sectors multiselect (default: Banking, Fertilizer)
- Excluded Sectors multiselect (default: Technology)
- Run AI Portfolio Optimization button (full width)
- Initial info box (hidden after first run)
- Success notification with Python list repr format
- 4 static metric cards (Expected Return, Risk, Dividend Yield, Method)
- Asset Allocation Pie Chart (Plotly.js, matches px.pie hole=0.4)
- Sector Distribution Bar Chart (Plotly.js, matches px.bar color="Sector")
- 5-Year Projected Growth Line Chart (dynamic on investment amount, green fill)
- Risk vs Return Scatter Plot (Plotly.js, matches px.scatter color="Portfolio")
- Optimization Comparison Table (st.dataframe equivalent)
- AI Explainability Module (st.info blue box, risk_appetite interpolated)
- Responsive layout (desktop/tablet/mobile)
