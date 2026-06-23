# Architecture

## Overview

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
        Customer-facing product page (demo frontend)
```

## Components

### 1. Data Pipeline
Ingests historical order data (timestamps, pincode, hub, courier, category, return reason, COD outcome) and produces engineered features per pincode-category pair.

### 2. Risk Prediction Model
Gradient-boosted model (XGBoost) trained to predict probability of delivery delay / return for a given pincode + category + season combination.

### 3. Root-Cause Classifier
Splits predicted risk into:
- **First-mile risk** — delay between order placement and dispatch (hub/warehouse-side)
- **Last-mile risk** — delay between dispatch and delivery (courier/area-side)

Initial version uses a rule-assisted threshold approach on timestamp deltas; explainability is prioritized over model complexity.

### 4. Confidence Score API
Exposes a 0-100 score with a breakdown of contributing factors, computed from model output.

### 5. Dynamic Delivery Promise API
Returns a delivery window calibrated to actual regional performance rather than a flat default estimate.

### 6. Nudge Recommendation Engine
Rule-based layer on top of model output — recommends actions (e.g., prepaid over COD) when risk crosses a threshold. Kept rule-based (not pure ML) for explainability and to avoid "black box" objections in review.

## Data Sources

See [`data-sources.md`](data-sources.md) for details on public datasets used and synthetic data generation approach, including honest disclosure of limitations.

## Fairness Safeguard

The system is designed so that a low confidence score triggers an intervention recommendation (alternate routing, buffer time, safer payment option) rather than a deprioritization signal — explicitly avoiding a feedback loop that would penalize already-underserved regions.
