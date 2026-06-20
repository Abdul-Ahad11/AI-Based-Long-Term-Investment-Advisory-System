# ai_investment_dss/logic_engine/text_matcher.py

class TokenTextMatcher:
    """Perception Layer: Extracts financial keywords from news text to determine truth values for core propositions."""
    
    def __init__(self):
        # Explicit domain vocabularies context-tuned for the Pakistan Stock Exchange (PSX)
        self.keywords_P = ["profit increase", "revenue growth", "expansion", "dividend increase", "production jump", "record earnings"]
        self.keywords_Q = ["net loss", "profit decline", "lawsuit", "debt increase", "default risk", "plant closure", "earnings drop"]
        self.keywords_R = ["sbp policy support", "secp approval", "tax relief", "export subsidy", "tariff hike protection"]
        self.keywords_S = ["inflation acceleration", "rupee devaluation", "imf constraints", "circular debt surge", "currency crisis"]

    def evaluate_propositions(self, text: str) -> dict:
        """
        Scans a text block and maps keyword discoveries to deterministic Boolean states.
        Returns a dictionary containing the truth value for each proposition.
        """
        normalized_text = text.lower().strip()
        
        # Proposition Assignment Logic via Exact Substring Token Verification
        p_state = any(token in normalized_text for token in self.keywords_P)
        q_state = any(token in normalized_text for token in self.keywords_Q)
        r_state = any(token in normalized_text for token in self.keywords_R)
        s_state = any(token in normalized_text for token in self.keywords_S)
        
        return {
            "P": p_state,  # Positive fundamentals
            "Q": q_state,  # Negative indicators
            "R": r_state,  # Regulatory tailwinds
            "S": s_state   # Macroeconomic risks
        }
