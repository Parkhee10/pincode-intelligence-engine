"""
Dynamic Delivery Promise endpoint.

NOTE: Placeholder logic — will be replaced by model-driven estimation
in Stage 1 once the risk model and historical delivery-time data exist.
"""
from fastapi import APIRouter, Query

from backend.api.schemas import DeliveryPromiseResponse

router = APIRouter()


def _mock_promise(pincode: str) -> DeliveryPromiseResponse:
    # TODO(stage-1): replace with real model-driven ETA estimation
    is_risky = pincode.endswith(("9", "0"))
    return DeliveryPromiseResponse(
        pincode=pincode,
        category="default",
        estimated_min_days=5 if is_risky else 2,
        estimated_max_days=8 if is_risky else 3,
        reliability_note=(
            "Delivery times in this area have been less consistent recently."
            if is_risky
            else "This area has a strong on-time delivery history."
        ),
    )


@router.get("/delivery-promise", response_model=DeliveryPromiseResponse)
def get_delivery_promise(
    pincode: str = Query(..., description="6-digit Indian pincode"),
    category: str = Query("default", description="Product category"),
):
    return _mock_promise(pincode)
