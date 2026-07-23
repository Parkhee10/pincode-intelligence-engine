delivery = '''import pandas as pd
from pathlib import Path
from functools import lru_cache
from datetime import datetime
from fastapi import APIRouter, Query
from backend.api.schemas import DeliveryPromiseResponse

router = APIRouter()
PINCODE_STATS_PATH = Path("data/sample/pincode_stats.csv")

@lru_cache(maxsize=1)
def _load_pincode_stats():
    df = pd.read_csv(PINCODE_STATS_PATH)
    df["pincode"] = df["pincode"].astype(str)
    return df.set_index("pincode").to_dict(orient="index")

def _is_festive_season():
    return datetime.now().month in (10, 11)

@router.get("/delivery-promise", response_model=DeliveryPromiseResponse)
def get_delivery_promise(
    pincode: str = Query(...),
    category: str = Query("apparel"),
):
    pincode_stats_map = _load_pincode_stats()
    if pincode not in pincode_stats_map:
        return DeliveryPromiseResponse(pincode=pincode, category=category, estimated_min_days=4, estimated_max_days=7, reliability_note="Limited history.")
    stats = pincode_stats_map[pincode]
    dispatch_hrs = stats.get("avg_dispatch_delay_hrs", 6.0)
    transit_hrs = stats.get("avg_transit_delay_hrs", 30.0)
    festive = _is_festive_season()
    total = (dispatch_hrs + transit_hrs) * (1.4 if festive else 1.0)
    min_days = max(1, int(total / 24))
    max_days = min_days + (2 if total > 48 else 1)
    if dispatch_hrs > 18:
        note = "Dispatch delays observed — buffer time added."
    elif transit_hrs > 50:
        note = "Transit times vary — order may arrive closer to later estimate."
    elif festive:
        note = "Festive season — extra buffer added."
    else:
        note = "This area has a reliable delivery history."
    return DeliveryPromiseResponse(pincode=pincode, category=category, estimated_min_days=min_days, estimated_max_days=max_days, reliability_note=note)
'''

nudge = '''import pandas as pd
from pathlib import Path
from functools import lru_cache
from fastapi import APIRouter, Query
from backend.api.schemas import NudgeResponse
from backend.core.config import settings

router = APIRouter()
PINCODE_STATS_PATH = Path("data/sample/pincode_stats.csv")

@lru_cache(maxsize=1)
def _load_pincode_stats():
    df = pd.read_csv(PINCODE_STATS_PATH)
    df["pincode"] = df["pincode"].astype(str)
    return df.set_index("pincode").to_dict(orient="index")

@router.get("/nudge", response_model=NudgeResponse)
def get_nudge(
    pincode: str = Query(...),
    order_value: float = Query(...),
):
    pincode_stats_map = _load_pincode_stats()
    if pincode not in pincode_stats_map:
        return NudgeResponse(pincode=pincode, order_value=order_value, nudge_triggered=False)
    stats = pincode_stats_map[pincode]
    cod_failure_rate = stats.get("cod_failure_rate", 0.03)
    return_rate = stats.get("return_rate", 0.08)
    if cod_failure_rate > 0.08:
        return NudgeResponse(pincode=pincode, order_value=order_value, nudge_triggered=True, recommended_action="prefer_prepaid", reason=f"COD issues common here ({cod_failure_rate:.0%} failure rate). Prepaid is more reliable.")
    if return_rate > 0.15 and order_value > 999:
        return NudgeResponse(pincode=pincode, order_value=order_value, nudge_triggered=True, recommended_action="check_size_guide", reason="Higher return rate here. Check size guide before ordering.")
    return NudgeResponse(pincode=pincode, order_value=order_value, nudge_triggered=False)
'''

with open('backend/api/routes/delivery_promise.py', 'w') as f:
    f.write(delivery)
with open('backend/api/routes/nudge.py', 'w') as f:
    f.write(nudge)
print("Done")