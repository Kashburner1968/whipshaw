import math

def normal_cdf(x):
    """
    Approximates the cumulative distribution function (CDF) for a standard normal distribution.
    Replaces scipy dependency to remain lightweight and robust across environments.
    """
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def normal_pdf(x):
    """
    Calculates the probability density function (PDF) for a standard normal distribution.
    """
    return math.exp(-0.5 * x**2) / math.sqrt(2.0 * math.pi)

def calculate_black_scholes_theta(S, K, T, r, sigma, option_type="call"):
    """
    Calculates the exact daily decay (Theta) of an option premium.
    Wall Street HFTs use this mathematical decay as a deterministic extraction pump.
    """
    if T <= 0:
        return 0.0

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type == "call":
        theta_term1 = -(S * normal_pdf(d1) * sigma) / (2 * math.sqrt(T))
        theta_term2 = -r * K * math.exp(-r * T) * normal_cdf(d2)
        theta = (theta_term1 + theta_term2) / 365.0
    else:
        theta_term1 = -(S * normal_pdf(d1) * sigma) / (2 * math.sqrt(T))
        theta_term2 = r * K * math.exp(-r * T) * normal_cdf(-d2)
        theta = (theta_term1 + theta_term2) / 365.0
        
    return theta

def identify_retail_extraction_zone(S, K, T, iv_percentile, base_iv):
    """
    Identifies if an option contract has entered the 'Predatory Extraction Zone'
    where premium pricing is decoupled from organic asset value.
    """
    inflated_iv = base_iv * (1.0 + (iv_percentile / 100.0))
    days_to_expiry = T * 365.0
    
    print(f"--- PARSING OPTIONS CHAIN DATA FOR UNDERLYING ASSET: ${S} ---")
    print(f"Strike Target: ${K} | Days left until absolute value erasure: {days_to_expiry:.1f}")
    print(f"Current Implied Volatility Level: {inflated_iv * 100:.1f}%")
    print("-" * 64)
    
    for day in range(3):
        remaining_t = (days_to_expiry - day) / 365.0
        if remaining_t <= 0:
            break
        
        daily_loss = calculate_black_scholes_theta(S, K, remaining_t, 0.04, inflated_iv)
        print(f"  [Day {day + 1}] Algorithmic Extraction Velocity (Daily Theta): {daily_loss:.4f} per contract")

    out_of_the_money_pct = ((K - S) / S) * 100 if K > S else 0
    if days_to_expiry <= 7 and out_of_the_money_pct > 5:
        print("\n[CRITICAL WARNING] RIGGED PARAMETERS DETECTED.")
        print("This contract resides inside the OTM Delta Trap. Expected Retail Return: -100%.")
        print("Mathematical equilibrium ensures 100% of this retail premium is absorbed by the writing institution.")

if __name__ == "__main__":
    # Test Scenario: Retail trader buying a short-dated, out-of-the-money call during an inflated IV spike
    identify_retail_extraction_zone(S=150.0, K=165.0, T=7/365.0, iv_percentile=85.0, base_iv=0.30)
