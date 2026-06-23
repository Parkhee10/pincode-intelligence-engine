# Pincode Intelligence Engine

> Predicting delivery risk, diagnosing its root cause, and intervening before the customer feels it.

[![Status](https://img.shields.io/badge/status-active%20development-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## The Problem

E-commerce trust isn't uniform — it varies sharply by geography. A 4.5-star product means little if buyers in *your* pincode routinely face late deliveries, COD failures, or difficult returns. Customers have no way to evaluate this regional risk before they buy, and platforms typically treat all regions as identical, surfacing generic "5-7 day" delivery estimates regardless of real, location-specific reliability.

This is especially costly in Tier 2/Tier 3 India, where delivery uncertainty is one of the biggest barriers between browse and buy — but it's also one of the least addressed problems in fashion-tech, because most teams focus on product-level signals (reviews, ratings) rather than geography-level ones.

## The Insight

Trust isn't one problem — it's multiple **cold-start problems**:
1. **Product cold-start** — new listings have no reviews
2. **Geography cold-start** — customers can't evaluate regional delivery/return risk before purchase
3. **Experience cold-start** — customers don't know what to expect (fit, delivery, authenticity)

This project tackles the most expensive and least-addressed of the three: **geography**.

## What This Does

Pincode Intelligence Engine doesn't just predict delivery risk — it diagnoses *why* the risk exists and recommends action before failure happens.

- **Risk Prediction** — likelihood of delay/return issues for a given pincode + product category
- **Root-Cause Diagnosis** — splits risk into **first-mile** (hub/dispatch delay) vs **last-mile** (courier/area issue)
- **Confidence Score** — a transparent, explainable score shown to the customer pre-purchase
- **Dynamic Delivery Promise** — a delivery estimate that reflects real regional reliability, not a flat default
- **Confidence-to-Action Nudges** — proactive suggestions (e.g. prepaid over COD) when risk is high

### A note on fairness

A naive version of this system risks creating a feedback loop — flagging a pincode as "low trust" and causing it to be deprioritized further, punishing exactly the underserved customers this is meant to help. This project is explicitly designed so that low scores trigger **intervention**, not **deprioritization**.

## Architecture

```
Historical order/delivery/return data
        │
        ▼
  Feature Pipeline (pincode, category, season, hub, courier)
        │
        ▼
  Risk Prediction Model (XGBoost)
        │
        ▼
  Root-Cause Classifier (first-mile vs last-mile)
        │
        ├──► Confidence Score API
        ├──► Dynamic Delivery Promise API
        └──► Nudge Recommendation Engine
                │
                ▼
        Customer-facing product page
```

Full architecture details: [`docs/architecture.md`](docs/architecture.md)

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Python, FastAPI |
| ML | scikit-learn, XGBoost |
| Data | pandas, public e-commerce/logistics datasets + synthetic augmentation |
| Frontend (demo) | React (mock product page) |
| DB | SQLite (hackathon scope) |

## Project Status

Actively under development for **Myntra WeForShe HackerRamp 2026** — Theme: *Speed & Trust*.

See [`docs/roadmap.md`](docs/roadmap.md) for milestones and current progress.

## Repository Structure

```
pincode-intelligence-engine/
├── docs/                  # Problem statement, architecture, data sources, roadmap
├── backend/
│   ├── api/               # FastAPI endpoints
│   ├── models/            # ML models (risk prediction, root-cause classifier)
│   ├── data_pipeline/     # Data sourcing + feature engineering
│   └── tests/
├── notebooks/exploratory/ # EDA notebooks
├── frontend/              # Demo product page
└── data/sample/           # Sample/synthetic data
```

## Getting Started

```bash
git clone https://github.com/<your-username>/pincode-intelligence-engine.git
cd pincode-intelligence-engine
# setup instructions added as backend is built
```

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT — see [`LICENSE`](LICENSE).
