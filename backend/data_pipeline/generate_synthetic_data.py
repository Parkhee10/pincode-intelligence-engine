"""
Synthetic data generator for the Pincode Intelligence Engine.

WHY THIS EXISTS:
We don't have access to real logistics data. This script generates a
realistic-but-synthetic dataset with deliberately injected pincode-level
reliability patterns.

Usage:
    python -m backend.data_pipeline.generate_synthetic_data
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

RANDOM_SEED = 42
N_PINCODES = 60
N_ORDERS = 15000
OUTPUT_DIR = Path("data/sample")
CATEGORIES = ["apparel", "footwear", "accessories", "beauty"]


class ReliabilityProfile(str, Enum):
    RELIABLE = "reliable"
    FIRST_MILE_RISK = "first_mile_risk"
    LAST_MILE_RISK = "last_mile_risk"
    BOTH_RISK = "both_risk"


@dataclass
class PincodeProfile:
    pincode: str
    hub_id: str
    courier_id: str
    profile: ReliabilityProfile
    dispatch_delay_mean: float
    dispatch_delay_std: float
    transit_delay_mean: float
    transit_delay_std: float
    cod_failure_rate: float
    base_return_rate: float


def _build_pincode_profiles(rng: np.random.Generator) -> list:
    profile_values = [p.value for p in ReliabilityProfile]
    weights = [0.55, 0.18, 0.18, 0.09]
    chosen = rng.choice(profile_values, size=N_PINCODES, p=weights)

    profiles = []
    for i in range(N_PINCODES):
        pincode = f"5{60000 + i * 7}"[:6]
        hub_id = f"HUB-{(i % 8) + 1:02d}"
        courier_id = f"COURIER-{(i % 12) + 1:02d}"
        profile = ReliabilityProfile(chosen[i])

        dispatch_mean, dispatch_std = 6.0, 2.0
        transit_mean, transit_std = 30.0, 8.0
        cod_failure_rate = 0.03
        base_return_rate = 0.08

        if profile == ReliabilityProfile.FIRST_MILE_RISK:
            dispatch_mean, dispatch_std = 30.0, 10.0
            base_return_rate = 0.14
        elif profile == ReliabilityProfile.LAST_MILE_RISK:
            transit_mean, transit_std = 70.0, 20.0
            cod_failure_rate = 0.13
            base_return_rate = 0.16
        elif profile == ReliabilityProfile.BOTH_RISK:
            dispatch_mean, dispatch_std = 26.0, 9.0
            transit_mean, transit_std = 65.0, 18.0
            cod_failure_rate = 0.15
            base_return_rate = 0.20

        jitter = rng.normal(1.0, 0.08)
        profiles.append(PincodeProfile(
            pincode=pincode,
            hub_id=hub_id,
            courier_id=courier_id,
            profile=profile,
            dispatch_delay_mean=max(2.0, dispatch_mean * jitter),
            dispatch_delay_std=dispatch_std,
            transit_delay_mean=max(10.0, transit_mean * jitter),
            transit_delay_std=transit_std,
            cod_failure_rate=min(0.9, max(0.01, cod_failure_rate * jitter)),
            base_return_rate=min(0.9, max(0.01, base_return_rate * jitter)),
        ))
    return profiles


def _simulate_orders(profiles: list, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    start_date = pd.Timestamp("2025-09-01")
    profile_by_pincode = {p.pincode: p for p in profiles}
    pincodes = [p.pincode for p in profiles]

    for order_idx in range(N_ORDERS):
        pincode = rng.choice(pincodes)
        p = profile_by_pincode[pincode]
        category = rng.choice(CATEGORIES)

        placed_offset_days = int(rng.integers(0, 270))
        placed_ts = start_date + pd.Timedelta(days=placed_offset_days)
        placed_ts += pd.Timedelta(hours=int(rng.integers(0, 24)))

        is_festive = pd.Timestamp(placed_ts).month in (10, 11)
        festive_multiplier = 1.4 if is_festive else 1.0

        dispatch_delay_hrs = max(0.5, float(rng.normal(p.dispatch_delay_mean, p.dispatch_delay_std)))
        transit_delay_hrs = max(2.0, float(rng.normal(p.transit_delay_mean, p.transit_delay_std)) * festive_multiplier)

        dispatched_ts = placed_ts + pd.Timedelta(hours=dispatch_delay_hrs)
        delivered_ts = dispatched_ts + pd.Timedelta(hours=transit_delay_hrs)

        is_cod = bool(rng.random() < 0.45)
        cod_failed = is_cod and bool(rng.random() < p.cod_failure_rate)

        total_delay_hrs = dispatch_delay_hrs + transit_delay_hrs
        delay_adjustment = min(0.25, total_delay_hrs / 400)
        return_prob = min(0.9, p.base_return_rate + delay_adjustment)
        is_returned = bool(rng.random() < return_prob)

        return_reason = None
        if is_returned:
            if dispatch_delay_hrs > p.dispatch_delay_mean * 1.3:
                return_reason = str(rng.choice(["late_dispatch", "changed_mind", "size_issue"], p=[0.5, 0.3, 0.2]))
            elif transit_delay_hrs > p.transit_delay_mean * 1.3:
                return_reason = str(rng.choice(["late_delivery", "damaged_in_transit", "changed_mind"], p=[0.5, 0.2, 0.3]))
            else:
                return_reason = str(rng.choice(["size_issue", "changed_mind", "quality_mismatch"], p=[0.4, 0.3, 0.3]))

        rows.append({
            "order_id": f"ORD{order_idx:06d}",
            "pincode": pincode,
            "hub_id": p.hub_id,
            "courier_id": p.courier_id,
            "category": category,
            "placed_ts": placed_ts,
            "dispatched_ts": dispatched_ts,
            "delivered_ts": delivered_ts,
            "dispatch_delay_hrs": round(dispatch_delay_hrs, 2),
            "transit_delay_hrs": round(transit_delay_hrs, 2),
            "is_cod": is_cod,
            "cod_failed": cod_failed,
            "is_returned": is_returned,
            "return_reason": return_reason,
            "_true_profile": p.profile.value,
        })

    return pd.DataFrame(rows)


def _build_pincode_stats(orders: pd.DataFrame) -> pd.DataFrame:
    agg = (
        orders.groupby("pincode")
        .agg(
            hub_id=("hub_id", "first"),
            courier_id=("courier_id", "first"),
            total_orders=("order_id", "count"),
            avg_dispatch_delay_hrs=("dispatch_delay_hrs", "mean"),
            avg_transit_delay_hrs=("transit_delay_hrs", "mean"),
            cod_failure_rate=("cod_failed", "mean"),
            return_rate=("is_returned", "mean"),
            true_profile=("_true_profile", "first"),
        )
        .reset_index()
    )
    agg["avg_dispatch_delay_hrs"] = agg["avg_dispatch_delay_hrs"].round(2)
    agg["avg_transit_delay_hrs"] = agg["avg_transit_delay_hrs"].round(2)
    agg["cod_failure_rate"] = agg["cod_failure_rate"].round(3)
    agg["return_rate"] = agg["return_rate"].round(3)
    return agg


def generate(output_dir: Path = OUTPUT_DIR) -> None:
    rng = np.random.default_rng(RANDOM_SEED)
    profiles = _build_pincode_profiles(rng)
    orders = _simulate_orders(profiles, rng)
    pincode_stats = _build_pincode_stats(orders)

    output_dir.mkdir(parents=True, exist_ok=True)
    orders.to_csv(output_dir / "orders.csv", index=False)
    pincode_stats.to_csv(output_dir / "pincode_stats.csv", index=False)

    print(f"Generated {len(orders)} orders across {len(profiles)} pincodes.")
    print(f"Written to: {output_dir}/orders.csv")
    print(f"Written to: {output_dir}/pincode_stats.csv")
    print("\nProfile distribution (ground truth):")
    print(pincode_stats["true_profile"].value_counts())


if __name__ == "__main__":
    generate()
