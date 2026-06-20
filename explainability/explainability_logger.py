# ai_investment_dss/explainability/explainability_logger.py

class ExplainabilityLogger:
    """Deterministic interpretation matrix converting quantitative scores into structured narrative text."""

    @staticmethod
    def get_metric_label(score: float, metric_name: str) -> str:
        """Maps standard 0-100 normalized scores to professional domain vocabulary."""
        if metric_name == "volatility":
            # Inverted scale: High score means low volatility (Safe)
            if score >= 75: return "Low Risk / High Price Stability"
            if score >= 40: return "Moderate Risk / Standard Fluctuations"
            return "Extreme Volatility / High Capital Risk"
            
        if score >= 80:
            return "Exceptional Performance (Top Tier)"
        if score >= 45:
            return "Stable / In-Line with Industry Average"
        return "Underperforming / Structural Weakness"

    @classmethod
    def generate_investment_rationale(cls, metrics_breakdown: dict, final_score: float, logic_modifier: int) -> str:
        """Compiles mathematical outputs and logic shocks into a clean analyst report."""
        norm = metrics_breakdown.get("normalized_metrics", {})
        
        # Determine macro rating profile
        if final_score >= 75:
            profile = "STRONG BUY (Highly Recommended)"
        elif final_score >= 50:
            profile = "HOLD (Neutral / Watchlist)"
        else:
            profile = "AVOID / SELL (High Risk / Weak Fundamentals)"

        report = []
        report.append("=" * 70)
        report.append(f"          EXPLAINABLE AI (XAI) AUTOMATED ANALYST REPORT          ")
        report.append("=" * 70)
        report.append(f"SYSTEM RECOMMENDATION PROFILE : {profile}")
        report.append(f"FINAL COMBINED SCORE          : {final_score} / 100")
        report.append(f"QUANTITATIVE BASELINE SCORE   : {metrics_breakdown.get('base_score')} / 100")
        report.append(f"QUALITATIVE NEWS MODIFIER     : {logic_modifier:+} points")
        report.append("-" * 70)
        report.append("A. HARD FUNDAMENTAL INSIGHTS (0-100 Metric Analysis):")
        
        for metric, val in norm.items():
            label = cls.get_metric_label(val, metric)
            clean_name = metric.replace("_", " ").title()
            report.append(f"  -> {clean_name:<17}: {val:>6} / 100 -> {label}")

        report.append("-" * 70)
        report.append("B. STRUCTURAL SUMMARY:")
        if final_score >= 75:
            report.append("  The asset exhibits highly defensive metrics with exceptional growth structures.")
            report.append("  Suitable for standard long-term capital preservation portfolios.")
        elif final_score >= 50:
            report.append("  The asset functions as an industry-standard baseline holding.")
            report.append("  Growth potentials are currently balanced out by active risks or volatility.")
        else:
            report.append("  Caution is highly advised. The mathematical scaling engine indicates")
            report.append("  depressed growth parameters, excessive leverage, or negative market shocks.")
        report.append("=" * 70)

        return "\n".join(report)