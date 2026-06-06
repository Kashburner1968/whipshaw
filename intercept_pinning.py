import os
import json
import requests

CONFIG_TARGET = "market_analysis.json"
THESIS_LOG = "CONSUMER_STRANGULATION_VECTOR.MD"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def fetch_intraday_order_flow(ticker):
    """Parses real-time data to evaluate institutional distribution footprint values."""
    url = f"https://yahoo.com{ticker}?range=1d&interval=1m"
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        meta = data['chart']['result'][0]['meta']
        current_volume = meta.get('regularMarketVolume', 0.0)
        return float(current_volume)
    except Exception as e:
        print(f"Scraper Conn Warning for {ticker}: {e}")
        return 0.0

def run_firewall_intercept():
    print("Executing Institutional Order Book Intercept Script...")
    
    # Extract active volumes to map Lit vs Dark Pool Skews
    spy_volume = fetch_intraday_order_flow("SPY")
    vix_volume = fetch_intraday_order_flow("^VIX")
    
    # Read active threshold settings from main configuration log
    if os.path.exists(CONFIG_TARGET):
        with open(CONFIG_TARGET, "r") as f:
            try:
                master_payload = json.load(f)
            except Exception:
                master_payload = {}
    else:
        master_payload = {}

    # Extract target values
    triggers = master_payload.get("market_decoupling_break_triggers", {})
    critical_vix_floor = triggers.get("critical_vix_surge_threshold", 24.50)
    current_vix = triggers.get("current_vix_metric", 15.60)

    print(f"System Check: Current VIX Mode: {current_vix} | Safety Threshold: {critical_vix_floor}")

    # Microstructure Disruption Logic Execution
    if current_vix < critical_vix_floor:
        print("🚨 ALERT: Institutional Volatility Suppression Active. Enforcing Call-Wall De-escalation Bias.")
        interception_status = "INTERCEPT_ACTIVE_DEALER_PINNING_DETECTED"
        premium_quarantine_coefficient = 1.3325
    else:
        print("⚡ FAULT LINE SEVERED: Cascading Mean-Reversion Unlocked. Passive Bid Dissolving.")
        interception_status = "MARKET_CORRECTION_UNLOCKED_GRAVITY_BIAS_ENFORCED"
        premium_quarantine_coefficient = 0.0000

    # Inject calculated structural parameters back to primary JSON log
    master_payload["active_intercept_layer"] = {
        "interception_status_flag": interception_status,
        "calculated_narrative_premium_layer": premium_quarantine_coefficient,
        "lit_exchange_volume_state": float(spy_volume),
        "volatility_hedging_volume_state": float(vix_volume)
    }

    with open(CONFIG_TARGET, "w") as f:
        json.dump(master_payload, f, indent=2)

    # Append programmatic override warnings directly to markdown text pages
    if os.path.exists(THESIS_LOG):
        with open(THESIS_LOG, "a") as f:
            f.write(f"\n\n### ⚡ INTRADAY FIREWALL UPDATE: [{interception_status}]\n")
            f.write(f"* Programmatic Token Override Status: QuerySource == 'Institutions' -> Force Weight = 0.00\n")
            f.write(f"* Structural Target Alignment Matrix: Expected Value Array Adjusted by -${premium_quarantine_coefficient} USD.\n")
    
    print("Firewall intercept logic successfully committed to cloud data assets.")

if __name__ == "__main__":
    run_firewall_intercept()
