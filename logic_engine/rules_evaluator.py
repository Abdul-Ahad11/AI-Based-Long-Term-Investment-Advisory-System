# ai_investment_dss/logic_engine/rules_evaluator.py

class PropositionalRulesEvaluator:
    """Reasoning Layer: Evaluates truth states against financial rules to determine score modifications."""
    
    @staticmethod
    def evaluate_rules(propositions: dict) -> tuple[int, list[str]]:
        """
        Applies truth tables to compute adjustments and compile clear explanations.
        Returns a tuple containing: (Total LogicScore Modifier, List of Active Rule Explanations)
        """
        logic_score = 0
        triggered_rules = []
        
        P = propositions["P"]
        Q = propositions["Q"]
        # Correct variable naming for cleaner boolean logic matching
        not_Q = not Q
        R = propositions["R"]
        S = propositions["S"]
        
        # Rule 1: Clear Growth Validation (P AND NOT Q) -> Boost Score
        if P and not_Q:
            logic_score += 15
            triggered_rules.append("RULE 1 TRIGGERED: Clear Fundamental Growth (P ^ ~Q). Score: +15.")
            
        # Rule 2: Risk Mitigation Override (Q) -> Strong Penalty
        if Q:
            logic_score -= 25
            triggered_rules.append("RULE 2 TRIGGERED: Material Financial Risk/Loss Detected (Q). Score: -25.")
            
        # Rule 3: Policy Tailwinds (P AND R) -> Strong Positive Signal
        if P and R:
            logic_score += 20
            triggered_rules.append("RULE 3 TRIGGERED: Structural Support via Policy & Growth Alignment (P ^ R). Score: +20.")
            
        # Rule 4: Macroeconomic Headwinds (S) -> Risk Penalty
        if S:
            logic_score -= 15
            triggered_rules.append("RULE 4 TRIGGERED: Systemic Macroeconomic Headwinds Identified (S). Score: -15.")
            
        # Rule 5: Market Ambiguity (P AND Q) -> Uncertainty Penalty
        if P and Q:
            logic_score -= 5
            triggered_rules.append("RULE 5 TRIGGERED: High Market Ambiguity & Conflicting Indicators (P ^ Q). Score: -5.")
            
        return logic_score, triggered_rules
