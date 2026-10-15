# Corporate and Institutional Market-Structure Investigation

**Mission:** Investigate and expose corporate and institutional practices that distort equity-market price discovery, obscure economic risks, or disadvantage households and smaller investors. Publish primary-source evidence, reproducible calculations, and clearly identified allegations.

## Core investigation: why can SPY rise amid equity fund outflows?

**Observed in the current Whipshaw dataset (week ending October 7, 2026):**
- Combined estimated equity fund flows: **−$11.406 billion**.
- Estimated bond fund flows: **+$24.527 billion**.
- Equity ETF net issuance reported in the related Whipshaw observation: **+$21.175 billion**.
- These flows differ by product and do not independently reveal the ultimate buyer, seller, or institutional ownership.

**Manipulation hypotheses under investigation:**
1. **Passive demand absorption:** recurring retirement-plan and index-fund allocations may absorb selling from other equity investors and reduce price sensitivity to deteriorating fundamentals.
2. **Dealer hedging and 0DTE effects:** option-market positioning and hedging may influence intraday volatility and strike-level price behavior. Deliberate price pinning is an allegation to investigate, not a conclusion established by options volume alone.
3. **Index concentration and sector masking:** strong performance in a few heavily weighted stocks or sectors may conceal negative breadth and weaker non-energy margins.
4. **Household–market divergence:** energy, debt-service and other essential expenses may weaken household purchasing power even when capitalization-weighted equity indexes rise.

## Evidence needed to identify actual misconduct

For each alleged mechanism, publish **who**, **what instrument**, **when**, **measurable price effect**, **source**, **alternative explanation**, and **degree of attribution**. Record regulatory findings, enforcement actions, and court filings separately from market-statistical inferences. Avoid naming a firm as having manipulated prices unless the specific allegation is backed by evidence.

## Falsifiable market tests

- Compare weekly ICI mutual fund and ETF flows with index returns; do not confuse issuance with intraday ETF purchases.
- Decompose SPY return by constituents/sectors and compare equal-weight performance and advance/decline breadth.
- Compare time-stamped options positioning, underlying prices, realized volatility, and hedging estimates, accounting for ordinary market-making.
- Test oil and diesel price shocks against reported corporate gross margins and real household expenditures using lags and controls.
- Publish negative findings and contrary evidence with the same prominence as supporting findings.

## Data contract

Every observation must contain: `observation_time`, `source_url`, `metric`, `value`, `units`, `method`, `status` (`observed`, `derived`, `hypothesis`, or `allegation`), and `limitations`. Missing data remain null; no synthetic real-time data or unsupported trade signals.

**Public-interest goal:** expose provable manipulation and its effects on price formation, without asserting that publication itself will force SPY to move in a particular direction.

Related machine-readable records:
- [Equity fund flows vs. ETF issuance](../observations/equity_exit_vs_etf_issuance_2026-10-15.json)
- [Market–household divergence](../research/market_household_divergence_2026-10-15.json)
- [Crude oil margin pressure](../research/crude_oil_margin_pressure_2026-10-15.json)
