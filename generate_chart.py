import os
import re
import pandas as pd
import matplotlib.pyplot as plt

def generate_trend_visualization():
    log_path = "liquidity_drain_log.md"
    output_image = "decoupling_trend.png"
    
    if not os.path.exists(log_path):
        print(f"Execution Error: {log_path} not found.")
        return

    # Parse structural rows from markdown table
    data_rows = []
    with open(log_path, "r") as f:
        for line in f:
            if line.startswith("|") and not re.search(r'[:---|-]', line) and "Date" not in line:
                # Clean table formatting tokens
                cells = [cell.strip().replace("$", "") for cell in line.split("|")[1:-1]]
                if len(cells) >= 6:
                    data_rows.append(cells)

    if not data_rows:
        print("Data Error: No structured log table rows parsed.")
        return

    # Construct analytical DataFrame
    df = pd.DataFrame(data_rows, columns=["Date", "SPY", "QQQ", "SPCX", "Ratio", "Delta"])
    df["Date"] = pd.to_datetime(df["Date"])
    df["SPY"] = pd.to_numeric(df["SPY"])
    df["QQQ"] = pd.to_numeric(df["QQQ"])
    df["Ratio"] = pd.to_numeric(df["Ratio"])

    # Calculate systemic divergence percentage baseline
    df["Divergence_Pct"] = ((df["Ratio"] - df["Ratio"].iloc[0]) / df["Ratio"].iloc[0]) * 100

    # Plot Construction
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = '#00ffcc'
    ax1.set_xlabel('Trading Session Timeline (2026)', fontsize=10, color='#888888')
    ax1.set_ylabel('SPY / QQQ Divergence Ratio', color=color, fontsize=10)
    ax1.plot(df["Date"], df["Ratio"], color=color, linewidth=2, label="Divergence Vector (SPY/QQQ)")
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', alpha=0.2)

    # Sub-plot for tracking relative divergence growth
    ax2 = ax1.twinx()  
    color = '#ff3366'
    ax2.set_ylabel('Accumulated Institutional Premium (%)', color=color, fontsize=10)
    ax2.fill_between(df["Date"], df["Divergence_Pct"], 0, where=(df["Divergence_Pct"] >= 0), 
                     color=color, alpha=0.15, label="Insulated Premium Margin")
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("INDEX COUPLING TREND: S&P 500 INSULATION VS. NASDAQ LIQUIDITY DRAIN", fontsize=12, pad=20)
    fig.tight_layout()
    
    # Export optimized static asset for GitHub UI rendering
    plt.savefig(output_image, dpi=300)
    plt.close()
    print(f"Analytics Asset Refreshed successfully: {output_image}")

if __name__ == "__main__":
    generate_trend_visualization()
