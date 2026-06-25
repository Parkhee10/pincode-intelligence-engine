"""
Confidence-to-Action Nudge endpoint.

Deliberately rule-based, not ML — explainability matters more than
sophistication here. This stub uses the threshold from settings; once
the real confidence score model exists, this will call it directly
instead of re-deriving risk locally.
"""
from fastapi import APIRouter, Query

from backend.api.schemas import NudgeResponse
from backend.core.config import settings

router = APIRouter()


@router.get("/nudge", response_model=NudgeResponse)
def get_nudge(
    pincode: str = Query(..., description="6-digit Indian pincode"),
    order_value: float = Query(..., description="Order value in INR"),
):
    # TODO(stage-1): call confidence score model instead of this placeholder rule
    is_risky = pincode.endswith(("9", "0"))

    if not is_risky:
        return NudgeResponse(
            pincode=pincode,
            order_value=order_value,
            nudge_triggered=False,
        )

    return NudgeResponse(
        pincode=pincode,
        order_value=order_value,
        nudge_triggered=True,
        recommended_action="prefer_prepaid",
        reason="This pincode has a history of COD delivery issues — prepaid orders are more reliable here.",
    )
