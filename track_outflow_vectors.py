import os
import json
import time
import yfinance as yf

def monitor_capital_rebalancing():
    log_file = "Systemic_Devaluation_Scenario_Log.json"
    
    # Core mega-cap cohort funding the IPO rotation pool
    tickers = ["SPY", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META"]
    
    print("[+] Initializing Microstructure Liquidity Tracker...")
    print(f"[+] Cohort Group: {tickers}")

    try:
        # Fetch current session real-time tick snapshots
        data_summary = {}
        for symbol in tickers:
            ticker_obj = yf.Ticker(symbol)
            # Pull 1-day historical data at 1-minute intervals
            snapshot = ticker_obj.history(period="1d", interval="1m")
            
            if not snapshot.empty:
                last_row = snapshot.iloc[-1]
                data_summary[symbol] = {
                    "price": float(round(last_row["Close"], 2)),
                    "volume": int(last_row["Volume"]),
                    "velocity_proxy": float(round(last_row["Close"] - snapshot.iloc[0]["Open"], 2))
                }
        
        # Calculate capital exhaustion metrics
        spy_metrics = data_summary.get("SPY", {"price": 1.0, "velocity_proxy": 0.0})
        log_payload = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event_id": "IPO-ROTATION-OUTFLOW-01",
            "narrative_trigger": "Pre-Listing Tech Capital Drainage Loop",
            "impact_metrics": {
                "spy_high": spy_metrics["price"],
                "spy_low": float(round(spy_metrics["price"] - abs(spy_metrics["velocity_proxy"]), 2)),
                "wti_crude_delta_pct": 0.0,
                "dow_jones_industrial_surge_points": 0
            },
            "microstructure_anomalies": {
                "liquidity_provision": "Tech_Liquidation_Pool",
                "hedging_vector": "Mega_Cap_Sell_To_Buy_Rotation",
                "cohort_snapshots": data_summary
            },
            "algorithmic_classification": "Institutional_Liquidity_Siphon",
            "downstream_risk_profile": "Index_Inflation_Under_Distribution"
        }

        # Step 2: Append payload to your valid log array
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                current_logs = json.load(f)
        else:
            current_logs = []

        current_logs.append(log_payload)

        with open(log_file, "w") as f:
            json.dump(current_logs, indent=2)

        print("[+] Structural Update Success: Capital outflow anomalies appended to log matrix.")

    except Exception as e:
        print(f"[-] Operational Exception: {str(e)}")

if __name__ == "__main__":
    monitor_capital_rebalancing()
