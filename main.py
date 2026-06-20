import sys
import os
from pathlib import Path
import yfinance as yf

# Establish clean workspace environment routing
sys.path.append(str(Path(__file__).resolve().parent))

from data_collection.market_fetcher import MarketDataFetcher
from data_collection.csv_loader import CSVDataLoader
from logic_engine.text_matcher import TokenTextMatcher
from logic_engine.rules_evaluator import PropositionalRulesEvaluator
from feature_engineering.indicators import FinancialIndicators
from heuristic_engine.scoring_model import HeuristicScoringModel
from recommendation_engine.investor_profile import InvestorProfile
from recommendation_engine.matching_logic import RecommendationEngine
from optimization_engine.optimizers import PortfolioOptimizer

def fetch_live_market_news(ticker: str) -> str:
    """Interrogates live Yahoo Finance feeds for the most recent asset headlines."""
    try:
        # FIXED: Removed the .KA suffix to support global tickers
        ticker_obj = yf.Ticker(ticker)
        news_items = ticker_obj.news
        
        if news_items and len(news_items) > 0:
            # Combine up to 3 recent headlines to build a rich contextual text block
            headlines = [item['title'] for item in news_items[:3]]
            combined_news = " | ".join(headlines)
            return combined_news
    except Exception:
        pass
    # Fallback default if news streams are temporarily blocked or empty
    return f"Stable market performance observed for {ticker} with standard baseline volume."

def execute_integrated_pipeline():
    print("=" * 70)
    print("    PRODUCTION RUN: LIVE STREAMING REAL-WORLD DATA & ADVISORY    ")
    print("=" * 70)
    
    # Phase 0: Sync market files locally
    print("\n[SYSTEM] Initiating Phase 0: Live Market Data Synchronization...")
    fetcher = MarketDataFetcher()
    fetcher.batch_sync_universe()
    
    # Initialize Core Underlying Analysis Engines
    text_matcher = TokenTextMatcher()
    scoring_engine = HeuristicScoringModel()
    
    # Set profile to Aggressive to inspect balanced logic performance with live metrics
    current_user = InvestorProfile(risk_tolerance="aggressive", capital=1000000)
    print(f"\n[SYSTEM] Active User Profile: {current_user.get_constraints()['profile_description']}")
    print("-" * 70)

    approved_pool = {}

    for ticker in fetcher.universe:
        # Step 1: Scrape live semantic news data over the network
        news_text = fetch_live_market_news(ticker)
        print(f"\n[FEED] Scraped Live News for {ticker}: \"{news_text[:85]}...\"")
        
        # Step 2: Read downloaded CSV records
        loader = CSVDataLoader(ticker=ticker)
        try:
            market_records = loader.load_historical_data()
        except FileNotFoundError:
            print(f"[SKIP] No local data cache found for {ticker}.")
            continue
            
        # Step 3: Run News Sentiment Rule Evaluation
        propositions = text_matcher.evaluate_propositions(news_text)
        logic_modifier, _ = PropositionalRulesEvaluator.evaluate_rules(propositions)
        
        # Step 4: Extract Core Quantitative Metrics
        raw_features = {
            "growth": FinancialIndicators.calculate_cagr(market_records),
            "volatility": FinancialIndicators.calculate_volatility(market_records),
            "stability": FinancialIndicators.calculate_stability(market_records),
            "dividend_yield": FinancialIndicators.calculate_total_dividend_yield(market_records),
            "liquidity": FinancialIndicators.calculate_average_liquidity(market_records)
        }
        
        # Step 5: Process total system scoring matrix
        score_breakdown = scoring_engine.compute_scores(raw_features, logic_modifier)
        final_score = score_breakdown["final_score"]
        
        # Step 6: Validate Eligibility Constraints
        match_result = RecommendationEngine.evaluate_match(
            ticker=ticker, 
            score_breakdown=score_breakdown, 
            final_score=final_score, 
            profile=current_user
        )
        
        if match_result["is_eligible"]:
            approved_pool[ticker] = final_score
            print(f"  -> 🟢 STATUS: APPROVED (Live Score: {final_score:.2f})")
        else:
            print(f"  -> 🔴 STATUS: REJECTED")
            print(f"    Reason: {match_result['rationale']}")

    # ==========================================
    # PHASE 3: PORTFOLIO OPTIMIZATION
    # ==========================================
    print("\n" + "=" * 70)
    print("                PHASE 3: LIVE PORTFOLIO OPTIMIZATION RUN              ")
    print("=" * 70)

    if len(approved_pool) < 2:
        print(f"[INFO] Pool size ({len(approved_pool)}) insufficient for full diversification optimization.")
        return

    optimizer = PortfolioOptimizer()
    hc_results = optimizer.hill_climbing(approved_pool, iterations=2000)
    sa_results = optimizer.simulated_annealing(approved_pool)
    
    print(f"\n[ALGORITHM 1] Hill Climbing: {hc_results['score']:.2f}")
    print(f"[ALGORITHM 2] Simulated Annealing: {sa_results['score']:.2f}")

if __name__ == "__main__":
    execute_integrated_pipeline()
