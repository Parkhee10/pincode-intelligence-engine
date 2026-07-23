content = '''import pandas as pd
from pathlib import Path
from functools import lru_cache
from datetime import datetime
from fastapi import APIRouter, Query
from backend.api.schemas import ConfidenceScoreResponse, RootCause
from backend.models.risk_model import predict as model_predict

router = APIRouter()
PINCODE_STATS_PATH = Path("data/sample/pincode_stats.csv")

@lru_cache(maxsize=1)
def _load_pincode_stats():
    df = pd.read_csv(PINCODE_STATS_PATH)
    df["pincode"] = df["pincode"].astype(str)
    return df.set_index("pincode").to_dict(orient="index")

def _is_festive_season():
    return datetime.now().month in (10, 11)

@router.get("/confidence-score", response_model=ConfidenceScoreResponse)
def get_confidence_score(
    pincode: str = Query(...),
    category: str = Query("apparel"),
):
    pincode_stats_map = _load_pincode_stats()
    if pincode not in pincode_stats_map:
        return ConfidenceScoreResponse(
            pincode=pincode,
            category=category,
            score=65.0,
            root_cause=RootCause.UNKNOWN,
            factors=["Limited delivery history for this pincode"],
        )
    stats = pincode_stats_map[pincode]
    stats["pincode"] = pincode
    result = model_predict(
        pincode_stats=stats,
        category=category,
        is_festive=_is_festive_season(),
    )
    return ConfidenceScoreResponse(
        pincode=pincode,
        category=category,
        score=result.confidence_score,
        root_cause=RootCause(result.root_cause.value),
        factors=result.factors,
    )
'''

with open('backend/api/routes/confidence.py', 'w') as f:
    f.write(content)
print("Done")