# ai_investment_dss/api.py
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path

# Fix routing so API can find your folders
sys.path.append(str(Path(__file__).resolve().parent))

# Import engines (Using the renamed MarketDataFetcher)
from data_collection.market_fetcher import MarketDataFetcher
from data_collection.csv_loader import CSVDataLoader
from logic_engine.text_matcher import TokenTextMatcher
from logic_engine.rules_evaluator import PropositionalRulesEvaluator
from feature_engineering.indicators import FinancialIndicators
from heuristic_engine.scoring_model import HeuristicScoringModel
from recommendation_engine.investor_profile import InvestorProfile
from recommendation_engine.matching_logic import RecommendationEngine
from optimization_engine.optimizers import PortfolioOptimizer
from main import fetch_live_market_news

# --- CONFIGURATION: GLOBAL SECTOR MAP ---
SECTOR_MAP = {
    # Technology
    "AAPL": "Technology", "MSFT": "Technology", "GOOGL": "Technology", "NVDA": "Technology",
    "META": "Technology", "ADBE": "Technology", "CSCO": "Technology", "CRM": "Technology",
    "ORCL": "Technology", "IBM": "Technology",
    
    # Finance
    "JPM": "Finance", "BAC": "Finance", "WFC": "Finance", "GS": "Finance",
    "MS": "Finance", "C": "Finance", "SCHW": "Finance", "AXP": "Finance",
    "USB": "Finance", "BLK": "Finance",
    
    # Healthcare
    "JNJ": "Healthcare", "PFE": "Healthcare", "MRK": "Healthcare", "ABBV": "Healthcare",
    "AMGN": "Healthcare", "UNH": "Healthcare", "CVS": "Healthcare", "LLY": "Healthcare",
    "BMY": "Healthcare", "GILD": "Healthcare",
    
    # Energy
    "XOM": "Energy", "CVX": "Energy", "COP": "Energy", "SLB": "Energy",
    "EOG": "Energy", "MPC": "Energy", "VLO": "Energy", "OXY": "Energy",
    "HES": "Energy", "DVN": "Energy",
    
    # Consumer Discretionary
    "AMZN": "Consumer", "TSLA": "Consumer", "HD": "Consumer", "MCD": "Consumer",
    "NKE": "Consumer", "DIS": "Consumer", "LOW": "Consumer", "BKNG": "Consumer",
    "SBUX": "Consumer", "GM": "Consumer",
    
    # Consumer Staples
    "PG": "Staples", "KO": "Staples", "PEP": "Staples", "COST": "Staples",
    "WMT": "Staples", "TGT": "Staples", "CL": "Staples", "EL": "Staples",
    "GIS": "Staples", "K": "Staples"
}

def get_sector(ticker: str) -> str:
    return SECTOR_MAP.get(ticker, "Unknown")

app = FastAPI(title="AI Investment DSS API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    capital: float
    risk_tolerance: str
    preferred_sectors: List[str] = []
    excluded_sectors: List[str] = []

@app.post("/api/run-pipeline")
def run_ai_pipeline(user_data: UserInput):
    try:
        current_user = InvestorProfile(
            risk_tolerance=user_data.risk_tolerance.lower(), 
            capital=user_data.capital
        )
        
        # Use updated MarketDataFetcher
        fetcher = MarketDataFetcher()
        fetcher.batch_sync_universe() 
        
        text_matcher = TokenTextMatcher()
        scoring_engine = HeuristicScoringModel()
        
        approved_assets = {}
        evaluation_matrix = []
        
        for ticker in fetcher.universe:
            ticker_sector = get_sector(ticker)
            
            # --- SECTOR FILTERING LOGIC ---
            if ticker_sector in user_data.excluded_sectors:
                continue 
            
            if user_data.preferred_sectors and ticker_sector not in user_data.preferred_sectors:
                continue

            news_text = fetch_live_market_news(ticker)
            
            try:
                loader = CSVDataLoader(ticker=ticker)
                market_records = loader.load_historical_data()
            except FileNotFoundError:
                continue

            propositions = text_matcher.evaluate_propositions(news_text)
            logic_modifier, _ = PropositionalRulesEvaluator.evaluate_rules(propositions)
            
            raw_features = {
                "growth": FinancialIndicators.calculate_cagr(market_records),
                "volatility": FinancialIndicators.calculate_volatility(market_records),
                "stability": FinancialIndicators.calculate_stability(market_records),
                "dividend_yield": FinancialIndicators.calculate_total_dividend_yield(market_records),
                "liquidity": FinancialIndicators.calculate_average_liquidity(market_records)
            }
            
            score_breakdown = scoring_engine.compute_scores(raw_features, logic_modifier)
            final_score = score_breakdown["final_score"]
            
            match_result = RecommendationEngine.evaluate_match(
                ticker=ticker, 
                score_breakdown=score_breakdown, 
                final_score=final_score, 
                profile=current_user
            )
            
            status = "approved" if match_result["is_eligible"] else "rejected"
            if match_result["is_eligible"]:
                approved_assets[ticker] = final_score
                
            evaluation_matrix.append({
                "ticker": ticker,
                "final_score": round(final_score, 2),
                "status": status,
                "xai_rationale": match_result["rationale"],
                "pillars": raw_features
            })

        # Phase 3: Optimization
        optimization_results = {"status": "insufficient_assets", "algorithm": None, "weights": {}}
        if len(approved_assets) >= 2:
            optimizer = PortfolioOptimizer()
            sa_results = optimizer.simulated_annealing(approved_assets)
            
            capital_allocation = {tck: round(weight * user_data.capital, 2) 
                                 for tck, weight in sa_results["weights"].items()}
                
            optimization_results = {
                "status": "optimized",
                "algorithm": "Simulated Annealing",
                "portfolio_score": sa_results["score"],
                "weights": sa_results["weights"],
                "capital_allocation_usd": capital_allocation # Renamed from PKR to USD
            }

        return {
            "user_profile": current_user.get_constraints(),
            "evaluation_matrix": evaluation_matrix,
            "optimization": optimization_results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
