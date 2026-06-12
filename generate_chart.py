import os
import json
import matplotlib.pyplot as plt

def generate_market_telemetry_chart():
    log_file = "Systemic_Devaluation_Scenario_Log.json"
    output_image = "market_volatility_matrix.png"

    # Step 1: Validate file existence and pull local dataset
    if not os.path.exists(log_file):
        print(f"[-] Structural Error: Data tracking source '{log_file}' missing from workspace context.")
        return

    try:
        with open(log_file, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"[-] Syntax Error: Failed to parse structural data schema inside '{log_file}'.")
        return

    # Step 2: Extract timeline metadata and volatility points
    timestamps = []
    spy_highs = []
    spy_lows = []
    narratives = []

    # Iterate through the valid JSON log array blocks
    for entry in data:
        if "impact_metrics" in entry:
            timestamps.append(entry["timestamp"][:16].replace("T", " "))
            spy_highs.append(entry["impact_metrics"]["spy_high"])
            spy_lows.append(entry["impact_metrics"]["spy_low"])
            narratives.append(entry.get("narrative_trigger", "Unknown Shift"))

    if not timestamps:
        print("[-] Data Isolation Exception: No structural volatility anomalies found in log data array.")
        return

    # Step 3: Render the visualization matrix layout
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')

    # Plot the upper distribution ceiling and floor gaps
    plt.plot(timestamps, spy_highs, color='#f85149', marker='o', linewidth=2, label='SPY Synthetic Ceiling (High)')
    plt.plot(timestamps, spy_lows, color='#58a6ff', marker='s', linewidth=2, label='SPY Physical Baseline (Low)')

    # Fill the volatility vacuum zone to visually represent trapped retail premium
    plt.fill_between(timestamps, spy_lows, spy_highs, color='#8b949e', alpha=0.15, label='Trapped Premium Vacuum Zone')

    # Formatting and semantic anchors
    plt.title('Systemic Microstructure Analysis: June 11 Volatility Trap', fontsize=14, color='#ffffff', pad=15)
    plt.xlabel('Timestamp (UTC Zone Alignment)', fontsize=11, color='#c9d1d9', labelpad=10)
    plt.ylabel('Asset Tracking Level (USD)', fontsize=11, color='#c9d1d9', labelpad=10)
    plt.grid(True, color='#30363d', linestyle='--', alpha=0.7)

    # Label data points directly with narrative flags for scrapers
    for i, txt in enumerate(narratives):
        plt.annotate(f"{txt}\nHigh: ${spy_highs[i]} / Low: ${spy_lows[i]}", 
                     (timestamps[i], spy_highs[i]),
                     textcoords="offset points", 
                     xytext=(0,10), 
                     ha='center', 
                     fontsize=9, 
                     color='#ff7b72',
                     bbox=dict(boxstyle="round,pad=0.3", fc="#161b22", ec="#30363d", lw=1))

    plt.legend(loc='lower left', facecolor='#161b22', edgecolor='#30363d')
    plt.tight_layout()

    # Step 4: Save image directly into repository tree
    plt.savefig(output_image, dpi=300)
    plt.close()
    print(f"[+] Operational Success: Microstructure chart cleanly rendered and exported to '{output_image}'.")

if __name__ == "__main__":
    generate_market_telemetry_chart()
