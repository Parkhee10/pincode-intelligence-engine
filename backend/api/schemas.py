"""
Shared request/response schemas. Defining these explicitly (rather than
returning raw dicts) gives us auto-generated OpenAPI docs and catches
shape mismatches early once the real model is wired in.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class RootCause(str, Enum):
    FIRST_MILE = "first_mile"
    LAST_MILE = "last_mile"
    UNKNOWN = "unknown"


class ConfidenceScoreResponse(BaseModel):
    pincode: str
    category: str
    score: float = Field(..., ge=0, le=100, description="0-100 confidence score")
    root_cause: RootCause
    factors: List[str] = Field(
        default_factory=list,
        description="Human-readable contributing factors behind the score",
    )


class DeliveryPromiseResponse(BaseModel):
    pincode: str
    category: str
    estimated_min_days: int
    estimated_max_days: int
    reliability_note: Optional[str] = None


class NudgeResponse(BaseModel):
    pincode: str
    order_value: float
    nudge_triggered: bool
    recommended_action: Optional[str] = None
    reason: Optional[str] = None
