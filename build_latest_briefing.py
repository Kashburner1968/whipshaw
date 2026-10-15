"""Produce a compact, continuously refreshed, source-linked machine-readable briefing."""
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent
def read(name):
    p=ROOT/name
    return json.loads(p.read_text()) if p.exists() else {}
def main():
    live=read("live_market_snapshot.json")
    changes=read("market_changes.json")
    if not live.get("metrics"):
        raise SystemExit("No live snapshot; briefing not published")
    metrics=live["metrics"]
    latest=[]
    for key, item in metrics.items():
        if not isinstance(item,dict) or item.get("value") is None:
            continue
        latest.append({"metric":key,"value":item["value"],"units":item.get("units"),"observed_at":item.get("observed_at"),"source_url":item.get("source_url"),"status":item.get("status","observed")})
    events=[
        {"title":"BlackRock Institute shifts U.S. equities to neutral and short Treasuries to overweight","date":"2026-10-12","path":"observations/blackrock_allocation_shift_2026-10-12.json"},
        {"title":"Headline retail sales vs. gasoline-excluded sales and oil price","date":"2026-10-15","path":"observations/retail_gasoline_spy_divergence_2026-10-15.json"}
    ]
    brief={"schema_version":"1.0","feed_id":"WHIPSHAW_RECURRING_MARKET_BRIEF","retrieved_at":live.get("retrieved_at"),
           "headline":"SPY, oil and market breadth proxies: latest observed prices and sourced context",
           "market_observations":latest,"recent_measured_changes":changes.get("findings",[]),
           "evidence_updates":events,
           "watch_questions":["Is SPY diverging from the equal-weight S&P 500 proxy RSP?",
                              "Is crude strengthening while SPY advances?",
                              "How do observed prices compare with published allocation and household-cost data?"],
           "interpretation":"These comparisons are research prompts, not verified explanations of intraday price causation.",
           "source_disclosure":"Public market quote provider; timestamps and delays vary. See per-metric provenance.",
           "refresh_target":"5-minute weekday collection, subject to provider and GitHub Actions execution"}
    out=ROOT/"latest_briefing.json"
    if out.exists():
        old=json.loads(out.read_text())
        if {k:v for k,v in old.items() if k!="retrieved_at"}=={k:v for k,v in brief.items() if k!="retrieved_at"}:
            return
    out.write_text(json.dumps(brief,indent=2)+"\n")
    print("Published machine-readable briefing",len(latest),"prices")
if __name__=="__main__":
    main()
