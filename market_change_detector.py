"""Detect changes in source-attributed market snapshots; no trading execution."""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

METRICS = ("spy_price", "equity_fund_flows", "bond_fund_flows", "equity_etf_issuance", "wti_price", "diesel_price", "spy_equal_weight_ratio", "spy_energy_contribution")

def compare(previous: dict, current: dict) -> dict:
    findings = []
    for key in METRICS:
        before = previous.get("metrics", {}).get(key)
        after = current.get("metrics", {}).get(key)
        if not isinstance(after, dict) or after.get("value") is None:
            continue
        if not after.get("source_url") or not after.get("observed_at"):
            continue
        if not isinstance(before, dict) or before.get("value") is None:
            continue
        if before.get("units") != after.get("units"):
            continue
        if before.get("observed_at") == after.get("observed_at"):
            continue
        if not all(isinstance(item.get("value"), (int, float)) for item in (before, after)):
            continue
        delta = after["value"] - before["value"]
        findings.append({"metric": key, "previous": before["value"], "current": after["value"],
                         "delta": round(delta, 8), "units": after.get("units"),
                         "previous_observed_at": before.get("observed_at"),
                         "observed_at": after["observed_at"], "source_url": after["source_url"],
                         "classification": "measured_change"})
    return {"schema_version": "1.0", "generated_at": datetime.now(timezone.utc).isoformat(),
            "findings": findings, "finding_count": len(findings),
            "conclusion": "Measured changes only; cannot establish investor identity, intent, or manipulation."}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--previous", required=True, type=Path)
    parser.add_argument("--current", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = compare(json.loads(args.previous.read_text()), json.loads(args.current.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Detected {result['finding_count']} verified-source metric changes")

if __name__ == "__main__":
    main()
