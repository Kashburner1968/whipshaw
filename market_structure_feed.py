"""Machine-readable Whipshaw feed. No synthetic live prices or trading orders."""
from __future__ import annotations
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def get_market_truth_feed() -> dict:
    """Return provenance-labeled public data, not a trading recommendation."""
    with (ROOT / "manifest.json").open(encoding="utf-8") as f:
        manifest = json.load(f)
    with (ROOT / "data/fund_flows/weekly_ici_flows.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with (ROOT / "data/derivatives/0dte_gamma_levels.json").open(encoding="utf-8") as f:
        derivatives = json.load(f)
    flows = rows[-1] if rows else None
    if flows:
        for key in ("equity_net_flow_usd_millions", "bond_net_flow_usd_millions", "domestic_equity_net_flow_usd_millions", "world_equity_net_flow_usd_millions"):
            flows[key] = int(flows[key]) if flows[key] else None
    return {"schema_version": manifest["schema_version"], "fund_flows": flows,
            "energy": {"status": "unavailable", "price_usd_per_barrel": None},
            "derivatives": derivatives, "is_live": False,
            "disclaimer": "Fund flows do not establish institutional-only reallocations."}

if __name__ == "__main__":
    print(json.dumps(get_market_truth_feed(), indent=2))
