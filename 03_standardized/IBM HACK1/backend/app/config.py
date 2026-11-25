import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RuralPulse — Healthcare Intelligence & Decision Support Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "karnataka-health-secret-key-super-secure-2026-nhm")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./karnataka_health.db")
    
    # Mode Configuration
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")
    
    # Datasets Path
    DATASETS_DIR: str = os.getenv("DATASETS_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "DATASETS")))
    
    # Groq LLM Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "groq/compound-mini")
    
    # IBM watsonx.ai Configuration
    WATSONX_API_KEY: str = os.getenv("WATSONX_API_KEY", "ff56489c-a4de-4982-bf0d-c3c0af11da72")
    WATSONX_PROJECT_ID: str = os.getenv("WATSONX_PROJECT_ID", "dc168c2e-7d58-4013-97f3-d258694789d9")
    WATSONX_DEPLOYMENT_ID: str = os.getenv("WATSONX_DEPLOYMENT_ID", "ff56489c-a4de-4982-bf0d-c3c0af11da72")
    WATSONX_URL: str = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    WATSONX_MODEL_ID: str = os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-8b-instruct")

    class Config:
        case_sensitive = True

settings = Settings()
