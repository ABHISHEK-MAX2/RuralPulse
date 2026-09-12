from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Karnataka Rural Healthcare Intelligence Platform"
    app_version: str = "1.0.0"
    environment: str = "demo"
    demo_mode: bool = True
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "karnataka_rural_healthcare_intelligence_secret_key_2026_prod"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    database_url: str = "sqlite:///./krhi.db"
    redis_url: str = ""
    cors_origins: str = "*"
    data_root: str = str(Path(__file__).resolve().parents[4])
    scoring_version: str = "v1.2.0-transparent-composite"
    rate_limit: str = "120/minute"
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
