"""Public market quote ingestion. Fail closed on stale, missing or malformed data."""
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "live_market_snapshot.json"
SYMBOLS = {"spy_price": "SPY", "wti_price": "CL=F", "equal_weight_price": "RSP", "energy_sector_price": "XLE"}
URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval=1m&range=1d"

def fetch(symbol):
    request = urllib.request.Request(URL.format(urllib.parse.quote(symbol, safe="")),
                                     headers={"User-Agent": "Mozilla/5.0 WhipshawMarketMonitor/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=18) as response:
        body = json.load(response)
    result = body["chart"]["result"][0]
    timestamps = result["timestamp"]
    closes = result["indicators"]["quote"][0]["close"]
    valid = [(int(t), float(p)) for t, p in zip(timestamps, closes) if p is not None and float(p) > 0]
    if not valid:
        raise ValueError("No valid observed prices")
    ts, value = valid[-1]
    if ts > time.time() + 120 or time.time() - ts > 86400:
        raise ValueError("Quote outside freshness window")
    return {"value": round(value, 6), "units": "USD", "observed_at": datetime.fromtimestamp(ts, timezone.utc).isoformat(),
            "source_url": URL.format(urllib.parse.quote(symbol, safe="")), "classification": "delayed_or_realtime_provider_quote",
            "provider": "Yahoo Finance chart endpoint", "exchange_delay_unknown": True}

def main():
    metrics = {}
    errors = {}
    for metric, symbol in SYMBOLS.items():
        try:
            metrics[metric] = fetch(symbol)
        except Exception as exc:
            errors[metric] = type(exc).__name__ + ": " + str(exc)[:180]
    if not metrics:
        raise SystemExit("No valid market observations; refusing to publish an empty snapshot: " + repr(errors))
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    for metric, record in old.get("metrics", {}).items():
        if metric not in metrics and isinstance(record, dict):
            # Missing fresh fetch is explicitly marked stale, not represented as current.
            metrics[metric] = {**record, "status": "stale_previous_observation"}
    new = {"schema_version": "1.0", "feed_id": "WHIPSHAW_MARKET_QUOTES", "is_live": True,
           "retrieved_at": datetime.now(timezone.utc).isoformat(), "metrics": metrics,
           "fetch_errors": errors, "warning": "Public provider quotes may be delayed. Not a consolidated SIP feed."}
    if old.get("metrics") == new["metrics"] and old.get("fetch_errors") == errors:
        print("No changes in quote data")
        return
    OUT.write_text(json.dumps(new, indent=2) + "\n")
    print("Published", len(metrics), "metrics;", len(errors), "errors")

if __name__ == "__main__":
    main()
