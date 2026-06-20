# ai_investment_dss/recommendation_engine/investor_profile.py

class InvestorProfile:
    """Models the human investor and defines mathematical constraints based on risk tolerance."""
    
    def __init__(self, risk_tolerance: str = "moderate", capital: float = 1000000.0, sector_pref: str = "none"):
        self.risk_tolerance = risk_tolerance.lower().strip()
        self.capital = capital
        self.sector_pref = sector_pref.lower().strip()

    def get_constraints(self) -> dict:
        """Returns the specific boundaries and thresholds required for this user profile."""
        if self.risk_tolerance == "conservative":
            return {
                "min_final_score": 65.0,
                "min_stability": 40.0,  # Requires high historical stability
                "min_volatility_score": 60.0, # High score means low risk/fluctuation
                "profile_description": "Conservative (Capital Preservation)"
            }
        elif self.risk_tolerance == "aggressive":
            return {
                "min_final_score": 50.0, # Willing to accept lower overall scores if growth is high
                "min_stability": 0.0,    # Does not care about historical drawdowns
                "min_volatility_score": 0.0, # Ignores volatility risks
                "profile_description": "Aggressive (High Risk / High Reward)"
            }
        else:
            # Default to Moderate
            return {
                "min_final_score": 60.0,
                "min_stability": 20.0,
                "min_volatility_score": 40.0,
                "profile_description": "Moderate (Balanced Growth)"
            }