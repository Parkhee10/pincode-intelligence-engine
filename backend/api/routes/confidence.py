"""
Confidence Score endpoint.

NOTE: This currently returns deterministic placeholder logic, not a real
model prediction. The risk model (Stage 1, next milestone) will replace
the `_mock_score` function below. Kept as a clearly-marked stub rather
than faking realistic-looking numbers, so the gap is honest and visible
in code review.
"""
from fastapi import APIRouter, Query

from backend.api.schemas import ConfidenceScoreResponse, RootCause

router = APIRouter()


def _mock_score(pincode: str) -> ConfidenceScoreResponse:
    # TODO(stage-1): replace with backend.models.risk_model.predict()
    is_risky = pincode.endswith(("9", "0"))  # arbitrary placeholder rule
    return ConfidenceScoreResponse(
        pincode=pincode,
        category="default",
        score=42.0 if is_risky else 88.0,
        root_cause=RootCause.LAST_MILE if is_risky else RootCause.UNKNOWN,
        factors=(
            ["Historically high last-mile delay in this pincode"]
            if is_risky
            else ["No significant risk signals found"]
        ),
    )


@router.get("/confidence-score", response_model=ConfidenceScoreResponse)
def get_confidence_score(
    pincode: str = Query(..., description="6-digit Indian pincode"),
    category: str = Query("default", description="Product category"),
):
    return _mock_score(pincode)
