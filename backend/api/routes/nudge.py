import pandas as pd
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
