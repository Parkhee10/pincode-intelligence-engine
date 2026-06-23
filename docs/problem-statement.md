# Problem Statement

## Context

Myntra serves millions of fashion customers across India, with significant growth potential in Tier 2/Tier 3 cities. For these customers, two factors stand between purchase intent and conversion: confidence that the product matches expectations, and confidence that delivery will be reliable.

## The Gap

Existing trust signals (ratings, reviews, generic delivery estimates) are **product-centric** and **region-agnostic**. They assume a customer's experience will be the same regardless of where they live. In reality:

- Delivery reliability varies significantly by pincode (hub proximity, courier partner coverage, local logistics infrastructure)
- COD success rates differ by region
- Return-to-origin friction differs by region
- None of this is visible to the customer at the moment of purchase decision

## Why This Matters

- **For customers:** delivery uncertainty is a top reason for cart abandonment in T2/T3 markets — customers don't know what they're risking when they hit "buy"
- **For Myntra:** undiagnosed regional delivery failures translate into return-to-origin costs, COD failure costs, and lost repeat customers — without clear visibility into *why* failures cluster in certain regions

## The Core Insight

Trust is not a single, uniform problem. It breaks down into multiple **cold-start problems**:

1. **Product cold-start** — new listings/sellers lack review history
2. **Geography cold-start** — customers cannot evaluate region-specific delivery/return risk before purchase
3. **Experience cold-start** — customers don't know what to expect across fit, delivery, and authenticity dimensions

This project addresses **geography cold-start** — the most operationally expensive and least-addressed of the three — by building a system that predicts regional delivery risk, diagnoses its root cause, and recommends intervention before failure occurs.

## Design Principle: No Punitive Feedback Loops

A risk-scoring system that simply flags "low-trust" pincodes risks creating a self-fulfilling loop — sellers and logistics deprioritizing already-underserved regions, making the problem worse. This system is explicitly designed so that a low score triggers an **intervention path** (alternate routing, buffer time, safer payment recommendation), not deprioritization.
