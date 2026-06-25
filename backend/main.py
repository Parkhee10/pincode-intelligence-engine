"""
Pincode Intelligence Engine — API entrypoint.

This is intentionally a thin entrypoint: app wiring only.
Business logic lives in routes/services, not here.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.api.routes import confidence, delivery_promise, nudge, health

app = FastAPI(
    title="Pincode Intelligence Engine",
    description=(
        "Predicts regional delivery risk, diagnoses its root cause "
        "(first-mile vs last-mile), and recommends interventions before "
        "delivery failure occurs."
    ),
    version="0.1.0",
)

# CORS left open for local frontend dev; tighten before any real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(confidence.router, prefix="/api/v1", tags=["confidence"])
app.include_router(delivery_promise.router, prefix="/api/v1", tags=["delivery-promise"])
app.include_router(nudge.router, prefix="/api/v1", tags=["nudge"])


@app.get("/")
def root():
    return {
        "service": "pincode-intelligence-engine",
        "status": "running",
        "docs": "/docs",
    }
