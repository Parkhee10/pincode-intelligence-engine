"""
Centralized configuration. Reads from environment variables with sane
defaults for local development. Avoid scattering os.environ calls
throughout the codebase — everything config-related goes through here.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_ENV: str = "development"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    DATABASE_URL: str = "sqlite:///./pie.db"

    # Thresholds used by the nudge engine — kept here, not hardcoded
    # in business logic, so they're tunable without touching code.
    RISK_SCORE_NUDGE_THRESHOLD: float = 60.0  # below this confidence score, trigger a nudge
    HIGH_RISK_THRESHOLD: float = 40.0

    class Config:
        env_file = ".env"


settings = Settings()
