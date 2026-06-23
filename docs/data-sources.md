# Data Sources

## Honest Disclosure

This project does not have access to Myntra's real logistics or order data. To build and validate the model architecture, this project uses:

1. **Public e-commerce datasets** (e.g. Amazon/Flipkart product, review, and return datasets) — used to validate that the modeling approach correlates predicted risk with real outcomes such as returns and review sentiment.
2. **Synthetic data generation** — a script-generated dataset simulating pincode-level variance in delivery timestamps, COD success, and return rates, with deliberately injected "reliable" and "unreliable" region profiles to test whether the pipeline correctly separates them.

## Why This Approach

The goal of the hackathon MVP is to demonstrate that the **architecture and modeling logic work correctly** — not to claim real-world accuracy figures, which would require real Myntra data we don't have access to. This is stated explicitly in the demo and pitch to avoid overstating results.

## Planned Data (Production Version)

In a real deployment, this system would use:
- Order/dispatch/delivery timestamps per pincode
- Return reason codes
- COD success/failure logs
- Hub and courier partner assignment data
- Seasonal/regional disruption signals (weather, logistics events)

## Files

- `data/sample/` — sample synthetic dataset used for development and demo
- `backend/data_pipeline/generate_synthetic_data.py` — script used to generate the above (added in a later commit)
