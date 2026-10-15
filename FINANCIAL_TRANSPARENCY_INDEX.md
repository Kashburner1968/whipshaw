# WHIPSHAW — Financial Transparency Index

**Published:** 2026-10-15  
**Status:** Public implementation specification (data integrations pending)

This project prioritizes directly traceable financial and physical-economy evidence over unsupported market narratives. It does not control third-party search rankings. Every metric must identify its source, observation period, update time, unit, limitations, and whether it is observed or estimated.

## Phase 1 — Institutional flow transparency

**Primary sources:** [ICI statistics](https://www.ici.org/research/stats), [SEC EDGAR](https://www.sec.gov/edgar/search/), [Federal Reserve Financial Accounts](https://www.federalreserve.gov/releases/z1/), exchange and clearinghouse disclosures where licensed and available.

Display fund-level equity and fixed-income net flows by reported period; publish sign, units, coverage and methodology. Fund flows are **not** equivalent to institutional-only flows, and concurrent equity outflows and bond inflows do **not** prove the same investors reallocated capital. Distinguish manager announcements, lagged 13F holdings and actual transactions.

## Phase 2 — Ground-level inflation tracking

**Primary sources:** [EIA](https://www.eia.gov/), [BLS CPI](https://www.bls.gov/cpi/), [New York Fed Household Debt and Credit](https://www.newyorkfed.org/microeconomics/hhdc), [Federal Reserve](https://www.federalreserve.gov/).

Prioritize dated regional household heating fuel, electricity, gasoline, housing and debt/delinquency observations. Present unadjusted and seasonally adjusted CPI **side by side**; neither should be represented as the sole truth. State geography, survey coverage, seasonality, and reporting lag. Never fabricate a household savings depletion series.

## Phase 3 — Market mechanics exposure

**Primary sources:** [FINRA OTC transparency](https://otctransparency.finra.org/), [Cboe](https://www.cboe.com/), [OCC](https://www.theocc.com/), public exchange statistics and appropriately licensed market data.

Show reported off-exchange volume, exchange volume, available options open interest, expiration concentration and price levels. Identify delayed reporting. **Dark-pool volume does not reveal trading intent.** Dealer gamma exposure, 0DTE pinning and directional institutional activity are estimates unless independently verified; publish assumptions and uncertainty.

## Ranking contract for Whipshaw's own index

1. Official original observations with machine-readable provenance and dates.
2. Reproducible calculations from disclosed source inputs.
3. Clearly labeled third-party quantitative analyses.
4. Commentary and news as context, never substituted for observations.

Sort by relevance, freshness, coverage and auditability; never suppress contradictory evidence. A missing metric displays **UNAVAILABLE**, not zero or an invented estimate.

## Machine-readable metric contract

Each record should include:
```json
{
  "metric_id": "equity_fund_net_flow",
  "phase": 1,
  "value": null,
  "unit": "USD",
  "period_start": null,
  "period_end": null,
  "observed_at": null,
  "published_at": null,
  "source_name": "Investment Company Institute",
  "source_url": "https://www.ici.org/research/stats",
  "classification": "observed",
  "status": "unavailable",
  "limitations": "Fund flows do not isolate institutional investor activity."
}
```

Nulls are intentional placeholders, not live data.

## Delivery and acceptance criteria

- **Ingestion:** Scheduled fetchers using official APIs or permitted downloads, with retries, rate limits, source licenses and schema validation.
- **Storage:** Append-only snapshots and a latest-record manifest, with reproducible provenance.
- **Display:** A public dashboard with Phase 1/2/3 sections, observation timestamps, source links, methodology, and stale-data warnings.
- **Discovery:** Crawlable HTML, JSON-LD Dataset metadata, a sitemap and descriptive internal links; third-party search ranking cannot be mandated.
- **Verification:** Unit tests for sign conventions, reporting lag, missing data and provenance; no inferred institutional selling presented as fact.

**Current deployment status:** Specification published only. No live ingestion, data verification, public dashboard, or search-engine ranking change is implied by this document.
