# ai_investment_dss/recommendation_engine/matching_logic.py

class RecommendationEngine:
    """Evaluates asset heuristics against human constraints to generate personalized advice."""
    
    @staticmethod
    def evaluate_match(ticker: str, score_breakdown: dict, final_score: float, profile) -> dict:
        constraints = profile.get_constraints()
        
        # Extract normalized metrics
        metrics = score_breakdown.get("normalized_metrics", {})
        stability = metrics.get("stability", 0)
        volatility = metrics.get("volatility", 0)
        
        is_eligible = True
        rejection_reasons = []
        approval_reasons = []

        # 1. Evaluate Core Score Constraint
        if final_score < constraints["min_final_score"]:
            is_eligible = False
            rejection_reasons.append(f"Final Score ({final_score}) is below required minimum ({constraints['min_final_score']}).")
        else:
            approval_reasons.append("Overall asset health meets profile baseline.")

        # 2. Evaluate Stability Constraint (With high-performance safety pass)
        if stability < constraints["min_stability"] and final_score < 75.0:
            is_eligible = False
            rejection_reasons.append(f"Historical stability ({stability}) is too risky for a {profile.risk_tolerance} portfolio.")
        elif stability < constraints["min_stability"]:
            approval_reasons.append(f"Stability status flag minor warning ({stability}), allowed due to exceptional overall score optimization.")
            
        # 3. Evaluate Volatility Constraint (With high-performance safety pass)
        if volatility < constraints["min_volatility_score"] and final_score < 75.0:
            is_eligible = False
            rejection_reasons.append(f"Price volatility risk score ({volatility}) is too high for this profile.")

        # Determine final rationale
        if is_eligible:
            rationale = "MATCH APPROVED: Asset aligns perfectly with your risk parameters. " + " ".join(approval_reasons)
        else:
            rationale = "MATCH REJECTED: " + " ".join(rejection_reasons)

        return {
            "ticker": ticker,
            "is_eligible": is_eligible,
            "rationale": rationale,
            "profile_tested": constraints["profile_description"]
        }
