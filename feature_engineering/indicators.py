# ai_investment_dss/feature_engineering/indicators.py

import math

class FinancialIndicators:
    """Pure mathematical layer to compute raw long-term financial features from historical data lists."""
    
    @staticmethod
    def calculate_cagr(records: list) -> float:
        """Computes the Compound Annual Growth Rate based on price history."""
        if len(records) < 2:
            return 0.0
        start_price = records[0]["close"]
        end_price = records[-1]["close"]
        
        days = (records[-1]["date"] - records[0]["date"]).days
        if days <= 0:
            return 0.0
        
        years = days / 365.25
        return (end_price / start_price) ** (1 / years) - 1 if start_price > 0 else 0.0

    @staticmethod
    def calculate_volatility(records: list) -> float:
        """Computes the standard deviation of daily log returns (historical volatility)."""
        if len(records) < 2:
            return 0.0
            
        returns = []
        for i in range(1, len(records)):
            prev_close = records[i-1]["close"]
            curr_close = records[i]["close"]
            if prev_close > 0 and curr_close > 0:
                returns.append(math.log(curr_close / prev_close))
                
        if len(returns) < 2:
            return 0.0
            
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
        return math.sqrt(variance)

    @staticmethod
    def calculate_stability(records: list) -> float:
        """Measures price stability as the inverse of Maximum Drawdown (MDD)."""
        if not records:
            return 0.0
            
        peak = -float('inf')
        max_drawdown = 0.0
        
        for record in records:
            close = record["close"]
            if close > peak:
                peak = close
            if peak > 0:
                drawdown = (peak - close) / peak
                if drawdown > max_drawdown:
                    max_drawdown = drawdown
                    
        # Return structural stability: 1.0 means 0 drawdown, lower values mean higher historic drops
        return 1.0 - max_drawdown

    @staticmethod
    def calculate_total_dividend_yield(records: list) -> float:
        """Calculates total dividends paid relative to the final closing asset price."""
        if not records:
            return 0.0
        latest_close = records[-1]["close"]
        if latest_close <= 0:
            return 0.0
        total_dividends = sum(r["dividends_paid"] for r in records)
        return total_dividends / latest_close

    @staticmethod
    def calculate_average_liquidity(records: list) -> float:
        """Computes Average Daily Trading Volume (ADTV)."""
        if not records:
            return 0.0
        return sum(r["volume"] for r in records) / len(records)