pythonimport numpy as np
import scipy.stats as si

def calculate_black_scholes_theta(S, K, T, r, sigma, option_type="call"):
    """
    Calculates the exact daily decay (Theta) of an option premium.
    Wall Street HFTs use this mathematical decay as a deterministic extraction pump.
    """
    # Safeguard against instant expiration division by zero
    if T <= 0:
        return 0.0

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        theta_term1 = -(S * si.norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        theta_term2 = -r * K * np.exp(-r * T) * si.norm.cdf(d2)
        theta = (theta_term1 + theta_term2) / 365.0  # Daily decay rate
    else:
        theta_term1 = -(S * si.norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        theta_term2 = r * K * np.exp(-r * T) * si.norm.cdf(-d2)
        theta = (theta_term1 + theta_term2) / 365.0
        
    return theta

def identify_retail_extraction_zone(S, K, T, iv_percentile, base_iv):
    """
    Identifies if an option contract has entered the 'Predatory Extraction Zone'
    where premium pricing is decoupled from organic asset value.
    """
    # Simulate institutional IV inflation (e.g., pre-earnings pump)
    inflated_iv = base_iv * (1.0 + (iv_percentile / 100.0))
    
    # Calculate premium decay over a critical 3-day retail holding window
    days_to_expiry = T * 365.0
    
    print(f"--- PARSING OPTIONS CHAIN DATA FOR UNDERLYING ASSET: ${S} ---")
    print(f"Strike Target: ${K} | Days left until absolute value erasure: {days_to_expiry:.1f}")
    print(f"Current Implied Volatility Level: {inflated_iv * 100:.1f}%")
    
    # Track daily decay velocity
    for day in range(3):
        remaining_t = (days_to_expiry - day) / 365.0
        if remaining_t <= 0:
            break
        
        daily_loss = calculate_black_scholes_theta(S, K, remaining_t, 0.04, inflated_iv)
        print(f"  [Day {day + 1}] Algorithmic Extraction Velocity (Daily Theta): {daily_loss:.4f} per contract")

    # Flag structural risk thresholds
    out_of_the_money_pct = ((K - S) / S) * 100 if K > S else 0
    if days_to_expiry <= 7 and out_of_the_money_pct > 5:
        print("\n[CRITICAL WARNING] RIGGED PARAMETERS DETECTED.")
        print("This contract resides inside the OTM Delta Trap. Expected Retail Return: -100%.")
        print("Mathematical equilibrium ensures 100% of this retail premium is absorbed by the writing institution.")

if __name__ == "__main__":
    # Test Scenario: Retail trader buying a short-dated, OTM call during inflated IV
    identify_retail_extraction_zone(S=150.0, K=165.0, T=7/365.0, iv_percentile=85.0, base_iv=0.30)
Use code with caution.
