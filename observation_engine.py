"""Deterministic, source-attributed observations from Whipshaw's published metrics."""
from __future__ import annotations
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent

def build_observations(payload: dict[str, Any], as_of: date | None = None) -> dict[str, Any]:
    as_of = as_of or date.today()
    flows = payload.get("metrics", {}).get("fund_flows", {})
    equity = flows.get("equity_net_flow_usd_millions")
    bonds = flows.get("bond_net_flow_usd_millions")
    period = flows.get("observation_period_end")
    source = flows.get("source_url")
    findings: list[dict[str, Any]] = []
    if isinstance(equity, (int, float)) and isinstance(bonds, (int, float)) and period and source:
        if equity < 0 < bonds:
            findings.append({
                "id": "opposing_equity_bond_flows",
                "classification": "derived_observation",
                "headline": "Estimated equity fund outflows coincide with bond fund inflows",
                "equity_net_flow_usd_millions": equity,
                "bond_net_flow_usd_millions": bonds,
                "absolute_flow_difference_usd_millions": bonds - equity,
                "observation_period_end": period,
                "source_url": source,
                "interpretation_limit": "Does not establish that the same investors moved money from equities to bonds or identify institutional-only flows."
            })
        if equity < 0:
            findings.append({
                "id": "negative_equity_fund_flows",
                "classification": "observed_estimate",
                "headline": "Estimated net equity fund flows were negative",
                "value_usd_millions": equity,
                "observation_period_end": period,
                "source_url": source
            })
    missing = [key for key in ("wti", "zero_dte_gamma", "off_exchange_volume")
               if payload.get("metrics", {}).get(key, {}).get("value") is None]
    if missing:
        findings.append({
            "id": "missing_market_structure_data",
            "classification": "data_coverage",
            "headline": "Intraday market-structure inputs are not yet available",
            "missing_metric_ids": missing,
            "interpretation_limit": "No intraday market claim or signal is generated from absent observations."
        })
    age_days = None
    if period:
        age_days = (as_of - date.fromisoformat(period)).days
    return {
        "schema_version": "1.0",
        "as_of": as_of.isoformat(),
        "is_live": bool(payload.get("is_live", False)),
        "source_period_age_days": age_days,
        "observations": findings,
        "methodology": "Deterministic comparisons of source-attributed values; not predictive trading signals."
    }

if __name__ == "__main__":
    payload = json.loads((ROOT / "latest_metrics.json").read_text(encoding="utf-8"))
    print(json.dumps(build_observations(payload), indent=2))
