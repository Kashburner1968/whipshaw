import os
import json
import matplotlib.pyplot as plt

def generate_fault_line_chart():
    config_file = "market_analysis.json"
    output_chart = "decoupling_trend.png"
    
    if not os.path.exists(config_file):
        print(f"Visualization Error: Configuration target {config_file} missing.")
        return

    with open(config_file, "r") as f:
        data = json.load(f)

    # Extract current computed parameters from JSON tracking fields
    triggers = data.get("market_decoupling_break_triggers", {})
    cascade = data.get("dehedging_cascade_parameters", {}).get("systemic_flip_indicators", {})

    vix_val = triggers.get("current_vix_metric", 15.6)
    vix_threshold = triggers.get("critical_vix_surge_threshold", 24.5)
    oi_drawdown = cascade.get("option_chain_open_interest_drawdown_pct", 0.0)
    tracking_err = cascade.get("passive_index_tracking_error_variance", 0.0)

    # Render Visual Framework
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Subplot 1: Volatility Acceleration Distance Mapping
    bars = ax1.bar(["Current VIX State", "Critical Trigger Floor"], [vix_val, vix_threshold], 
                   color=['#00ffcc', '#ff3366'], width=0.5, edgecolor='#ffffff', alpha=0.8)
    ax1.set_ylabel('Volatility Measurement Units', fontsize=10)
    ax1.set_title('MACRO VOLATILITY BREAK TRIGGER DISTANCE', fontsize=11, pad=15)
    ax1.grid(True, linestyle=':', alpha=0.3)
    # Highlight the absolute boundary values
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{height}', ha='center', va='bottom', color='#ffffff')

    # Subplot 2: Structural Option Flow Decay Matrix
    metrics = ["Call Wall OI Decay", "Passive Tracking Variance"]
    values = [abs(oi_drawdown), tracking_err * 100] # Scale tracking variance for clarity
    
    ax2.barh(metrics, values, color=['#ff9900', '#3399ff'], height=0.4, edgecolor='#ffffff', alpha=0.8)
    ax2.set_xlabel('Calculated Instability Multiplier (%)', fontsize=10)
    ax2.set_title('STRUCTURAL DEHEDGING & OPTION POOL DISTORTION', fontsize=11, pad=15)
    ax2.grid(True, linestyle=':', alpha=0.3)

    plt.suptitle("DECOUPLING CORE VECTOR: INSTITUTIONAL PRICE PINNING BREAKPOINTS", fontsize=13, y=0.98)
    plt.tight_layout()
    
    # Save optimized visualization layout asset
    plt.savefig(output_chart, dpi=300)
    plt.close()
    print(f"Microstructure chart metric refreshed successfully: {output_chart}")

if __name__ == "__main__":
    generate_fault_line_chart()
