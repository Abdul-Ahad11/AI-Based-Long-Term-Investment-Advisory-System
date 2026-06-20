# ai_investment_dss/heuristic_engine/scoring_model.py

from config.settings import HEURISTIC_WEIGHTS

class HeuristicScoringModel:
    """Applies corporate min-max normalization, weighs structural features, and merges logic scores."""
    
    def __init__(self):
        self.weights = HEURISTIC_WEIGHTS
        
        # FIXED: Adjusted boundaries to seamlessly support high-volume, high-growth US global equities
        self.bounds = {
            "growth": {"min": -0.30, "max": 0.50},         # -30% to +50% CAGR to capture tech rallies/corrections
            "stability": {"min": 0.00, "max": 1.00},      # Reset to 0.0 floor so historical drawdowns don't force a 0 score
            "dividend_yield": {"min": 0.00, "max": 0.10},   # 0% to 10% typical dividend scales
            "volatility": {"min": 0.00, "max": 0.06},       # Adjusted to properly scale US equity daily log return volatility
            "liquidity": {"min": 10000, "max": 50000000}    # Expanded scale up to 50M to support massive US trading volumes
        }

    def _normalize(self, value: float, metric: str) -> float:
        """Maps raw values to a consistent 0 to 100 scale using min-max bounds."""
        b = self.bounds.get(metric)
        if not b:
            return 50.0 # Neutral fallback flag
            
        if value <= b["min"]:
            return 0.0 if metric != "volatility" else 100.0
        if value >= b["max"]:
            return 100.0 if metric != "volatility" else 0.0
            
        # Volatility is a risk feature: higher volatility results in a lower score
        if metric == "volatility":
            return 100.0 - ((value - b["min"]) / (b["max"] - b["min"]) * 100)
            
        return (value - b["min"]) / (b["max"] - b["min"]) * 100

    def compute_scores(self, raw_features: dict, logic_score_modifier: int) -> dict:
        """
        Processes raw metrics into a weighted BaseScore and applies the LogicScore modifier.
        Returns a complete, explainable score breakdown.
        """
        # 1. Normalize all inputs
        norm_g = self._normalize(raw_features["growth"], "growth")
        norm_st = self._normalize(raw_features["stability"], "stability")
        norm_d = self._normalize(raw_features["dividend_yield"], "dividend_yield")
        norm_v = self._normalize(raw_features["volatility"], "volatility")
        norm_l = self._normalize(raw_features["liquidity"], "liquidity")
        norm_se = 65.0  # Placeholder representing sector median strength
        
        # 2. Compute the weighted BaseScore
        base_score = (
            (norm_g * self.weights["growth"]) +
            (norm_st * self.weights["stability"]) +
            (norm_d * self.weights["dividend_yield"]) +
            (norm_v * self.weights["volatility"]) +
            (norm_l * self.weights["liquidity"]) +
            (norm_se * self.weights["sector_strength"])
        )
        
        # 3. Apply LogicScore modifier and enforce strict [0, 100] bounds
        final_score = max(0.0, min(100.0, base_score + logic_score_modifier))
        
        return {
            "base_score": round(base_score, 2),
            "final_score": round(final_score, 2),
            "normalized_metrics": {
                "growth": round(norm_g, 2),
                "stability": round(norm_st, 2),
                "dividend_yield": round(norm_d, 2),
                "volatility": round(norm_v, 2),
                "liquidity": round(norm_l, 2),
                "sector_strength": round(norm_se, 2)
            }
        }
