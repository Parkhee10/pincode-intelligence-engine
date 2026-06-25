"""Health check endpoint — used for deployment readiness checks later."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}
