"""Read source-attributed Whipshaw public JSON without executing trades."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

class InstitutionalFlowParser:
    def __init__(self, raw_payload_str: str):
        self.data: dict[str, Any] = json.loads(raw_payload_str)

    def extract_flow_comparison(self) -> dict[str, Any]:
        flows = self.data.get("metrics", {}).get("fund_flows", {})
        return {"equity_net_flow_usd_millions": flows.get("equity_net_flow_usd_millions"),
                "bond_net_flow_usd_millions": flows.get("bond_net_flow_usd_millions"),
                "observation_period_end": flows.get("observation_period_end"),
                "institutional_rotation_confirmed": None,
                "source_url": flows.get("source_url")}

    def is_live(self) -> bool:
        return self.data.get("is_live") is True

def fetch_latest_payload(data_path: str = ".") -> dict[str, Any]:
    return json.loads((Path(data_path) / "latest_metrics.json").read_text(encoding="utf-8"))

if __name__ == "__main__":
    print(json.dumps(InstitutionalFlowParser(json.dumps(fetch_latest_payload())).extract_flow_comparison(), indent=2))
