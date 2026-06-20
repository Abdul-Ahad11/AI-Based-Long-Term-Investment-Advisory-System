import sys
import time
from pathlib import Path
import yfinance as yf
import pandas as pd

# Connect context back to project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.settings import RAW_MARKET_DIR, TARGET_TICKERS

class MarketDataFetcher:
    """Automates real-world historical OHLCV data extraction for global markets using yfinance."""
    
    def __init__(self):
        RAW_MARKET_DIR.mkdir(parents=True, exist_ok=True)
        # CRITICAL FIX: Define universe so main.py can seamlessly loop through it
        self.universe = TARGET_TICKERS
        
    def fetch_ticker_data(self, ticker: str) -> bool:
        """
        Downloads daily historical data securely using yfinance.
        """
        clean_ticker = ticker.strip().upper()
        output_path = RAW_MARKET_DIR / f"{clean_ticker}.csv"
        
        print(f"[FETCHING] Querying secure yfinance channel for {clean_ticker}...")
        
        try:
            # Restrict period to 2y for realistic active tracking and stability metrics
            ticker_obj = yf.Ticker(clean_ticker)
            df = ticker_obj.history(period="2y")
            
            # Fallback wrapper if the primary history stream is empty
            if df.empty:
                df = yf.download(clean_ticker, period="2y", progress=False)
                
            if df.empty:
                print(f"[ERROR] Asset validation failed or no data returned for '{clean_ticker}'.")
                return False
                
            # Flatten the index so 'Date' becomes a standard column for our csv_loader
            df.reset_index(inplace=True)
            
            # Format the Date column to YYYY-MM-DD cleanly
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            
            # Save cleanly to CSV without the pandas index column
            df.to_csv(output_path, index=False)
            print(f"[SUCCESS] Saved raw data file directly to: {output_path}")
            return True
            
        except Exception as e:
            print(f"[CRITICAL] Unexpected data stream collapse: {e}")
            return False

    def batch_sync_universe(self):
        """Runs sequential data harvests across your entire system asset scope."""
        print("=" * 60)
        print("        LAUNCHING REAL-TIME MARKET ACQUISITION ENGINE         ")
        print("=" * 60)
        print(f"Target Assets Outlined in Settings: {self.universe}\n")
        
        success_count = 0
        for ticker in self.universe:
            # Polite scraping cadence to avoid being rate-limited by Yahoo
            time.sleep(1.0)
            if self.fetch_ticker_data(ticker):
                success_count += 1
                
        print("-" * 60)
        print(f"[STATUS] Pipeline Synced. Successfully harvested {success_count}/{len(self.universe)} assets.")
        print("=" * 60)

if __name__ == "__main__":
    fetcher = MarketDataFetcher()
    fetcher.batch_sync_universe()
