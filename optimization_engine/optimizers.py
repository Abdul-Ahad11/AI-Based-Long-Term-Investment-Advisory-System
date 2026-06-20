import random
import math

class PortfolioOptimizer:
    def __init__(self):
        pass

    def _is_valid(self, weights):
        """Helper method to check if the weights satisfy all constraints."""
        for w in weights.values():
            if w < 0.05 or w > 0.60:
                return False
        # Check if the sum is effectively 1.0 (accounting for floating-point precision)
        return abs(sum(weights.values()) - 1.0) < 1e-5

    def _calculate_portfolio_score(self, weights, approved_pool):
        """Helper method to calculate the weighted objective score."""
        return sum(weights[ticker] * approved_pool[ticker] for ticker in weights)

    def _generate_initial_weights(self, tickers):
        """Generates an even distribution of weights as a valid starting point."""
        n = len(tickers)
        if n == 0:
            return {}
        
        # Safe fallback: If only 1 asset is approved, it must take 100% despite the 60% rule
        if n == 1:
            return {tickers[0]: 1.0}
            
        equal_weight = 1.0 / n
        return {ticker: equal_weight for ticker in tickers}

    def hill_climbing(self, approved_pool, iterations=1000):
        """
        Maximizes portfolio score using the Hill Climbing local search algorithm.
        Only moves to a neighbor if the portfolio score is strictly higher.
        """
        tickers = list(approved_pool.keys())
        if not tickers:
            return {"weights": {}, "score": 0.0}
        
        # Handle edge case where optimization isn't needed
        if len(tickers) == 1:
            return {"weights": {tickers[0]: 1.0}, "score": approved_pool[tickers[0]]}

        # Initialize state
        current_weights = self._generate_initial_weights(tickers)
        current_score = self._calculate_portfolio_score(current_weights, approved_pool)

        for _ in range(iterations):
            # Tweak: Pick two random assets and shift a tiny fraction of weight between them
            ticker_a, ticker_b = random.sample(tickers, 2)
            step = 0.01  # 1% shift
            
            # Create a candidate neighbor
            neighbor_weights = current_weights.copy()
            neighbor_weights[ticker_a] += step
            neighbor_weights[ticker_b] -= step

            # If the shift violates our 5% min or 60% max boundaries, skip it
            if not self._is_valid(neighbor_weights):
                continue

            # Evaluate neighbor
            neighbor_score = self._calculate_portfolio_score(neighbor_weights, approved_pool)

            # Hill Climbing rule: Accept only if strictly better
            if neighbor_score > current_score:
                current_weights = neighbor_weights
                current_score = neighbor_score

        # Round weights for clean output presentation
        cleaned_weights = {k: round(v, 4) for k, v in current_weights.items()}
        return {"weights": cleaned_weights, "score": round(current_score, 2)}

    def simulated_annealing(self, approved_pool, initial_temp=10.0, cooling_rate=0.995, iterations=2000):
        """
        Maximizes portfolio score using Simulated Annealing.
        Allows probabilistic acceptance of worse scores early on to escape local maxima.
        """
        tickers = list(approved_pool.keys())
        if not tickers:
            return {"weights": {}, "score": 0.0}
            
        if len(tickers) == 1:
            return {"weights": {tickers[0]: 1.0}, "score": approved_pool[tickers[0]]}

        # Initialize state
        current_weights = self._generate_initial_weights(tickers)
        current_score = self._calculate_portfolio_score(current_weights, approved_pool)
        
        best_weights = current_weights.copy()
        best_score = current_score
        
        temp = initial_temp

        for _ in range(iterations):
            if temp <= 0.01:
                break

            # Tweak: Pick two random assets and shift a tiny fraction of weight
            ticker_a, ticker_b = random.sample(tickers, 2)
            step = 0.01
            
            neighbor_weights = current_weights.copy()
            neighbor_weights[ticker_a] += step
            neighbor_weights[ticker_b] -= step

            if not self._is_valid(neighbor_weights):
                continue

            neighbor_score = self._calculate_portfolio_score(neighbor_weights, approved_pool)
            score_diff = neighbor_score - current_score

            # Simulated Annealing rule: Accept if better, OR accept with probability if worse
            if score_diff > 0:
                current_weights = neighbor_weights
                current_score = neighbor_score
            else:
                # Probability formula: e^(delta / temp)
                acceptance_probability = math.exp(score_diff / temp)
                if random.random() < acceptance_probability:
                    current_weights = neighbor_weights
                    current_score = neighbor_score

            # Keep track of the absolute best global configuration found so far
            if current_score > best_score:
                best_weights = current_weights.copy()
                best_score = current_score

            # Cool down the system
            temp *= cooling_rate

        cleaned_weights = {k: round(v, 4) for k, v in best_weights.items()}
        return {"weights": cleaned_weights, "score": round(best_score, 2)}


# ==========================================
# VERIFICATION BLOCK (Runs standalone test)
# ==========================================
if __name__ == "__main__":
    print("--- Testing PortfolioOptimizer Standalone ---")
    
    # Simulating a mock approved pool generated from Phase 2
    mock_approved_pool = {
        "SYS": 85.5,
        "EFERT": 62.1,
        "ENGRO": 78.4,
        "HUBC": 91.2
    }
    
    optimizer = PortfolioOptimizer()
    
    print(f"Mock Approved Assets & Scores: {mock_approved_pool}\n")
    
    # Test Hill Climbing
    hc_result = optimizer.hill_climbing(mock_approved_pool)
    print(" [1] Hill Climbing Allocation Result:")
    print(f"    Weights: {hc_result['weights']}")
    print(f"    Expected Portfolio Score: {hc_result['score']}\n")
    
    # Test Simulated Annealing
    sa_result = optimizer.simulated_annealing(mock_approved_pool)
    print(" [2] Simulated Annealing Allocation Result:")
    print(f"    Weights: {sa_result['weights']}")
    print(f"    Expected Portfolio Score: {sa_result['score']}\n")
    
    # Verify Constraints sanity check
    total_weight = sum(sa_result['weights'].values())
    print(f"Constraint Check -> Total Allocation Sum: {total_weight:.2f} (Should be exactly 1.0)")
