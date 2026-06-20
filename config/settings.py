from pathlib import Path

# Base Directory Resolve
BASE_DIR = Path(__file__).resolve().parent.parent

# Data Path Configurations
RAW_MARKET_DIR = BASE_DIR / "data" / "raw_market"
RAW_NEWS_DIR = BASE_DIR / "data" / "raw_news"

# Project Scope Parameters (Global Target Universe)
TARGET_TICKERS = [
    # Technology
    "AAPL", "MSFT", "GOOGL", "NVDA", "META", "ADBE", "CSCO", "CRM", "ORCL", "IBM",
    # Finance
    "JPM", "BAC", "WFC", "GS", "MS", "C", "SCHW", "AXP", "USB", "BLK",
    # Healthcare
    "JNJ", "PFE", "MRK", "ABBV", "AMGN", "UNH", "CVS", "LLY", "BMY", "GILD",
    # Energy
    "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "VLO", "OXY", "HES", "DVN",
    # Consumer Discretionary
    "AMZN", "TSLA", "HD", "MCD", "NKE", "DIS", "LOW", "BKNG", "SBUX", "GM",
    # Consumer Staples
    "PG", "KO", "PEP", "COST", "WMT", "TGT", "CL", "EL", "GIS", "K"
]

# Heuristic Weight Configurations (Must sum to 1.0)
HEURISTIC_WEIGHTS = {
    "growth": 0.25,
    "stability": 0.20,
    "dividend_yield": 0.20,
    "volatility": 0.15,
    "sector_strength": 0.10,
    "liquidity": 0.10
}
