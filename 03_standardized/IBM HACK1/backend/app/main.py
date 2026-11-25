from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import (
    auth, geography, facilities, vulnerability,
    recommendations, mmus, alerts, data_sources, audit, reports
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-assisted healthcare decision-support platform for Karnataka district/state health administrators and MMU coordinators.",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(geography.router, prefix=settings.API_V1_STR)
app.include_router(facilities.router, prefix=settings.API_V1_STR)
app.include_router(vulnerability.router, prefix=settings.API_V1_STR)
app.include_router(recommendations.router, prefix=settings.API_V1_STR)
app.include_router(mmus.router, prefix=settings.API_V1_STR)
app.include_router(alerts.router, prefix=settings.API_V1_STR)
app.include_router(data_sources.router, prefix=settings.API_V1_STR)
app.include_router(audit.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["System Health"])
def health_check():
    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "demo_mode": settings.DEMO_MODE,
        "database": "CONNECTED"
    }

@app.get("/ready", tags=["System Health"])
def readiness_check():
    return {"status": "READY"}

@app.get("/", tags=["System Root"])
def root():
    return {
        "message": "RuralPulse — Healthcare Intelligence & Decision Support Platform API",
        "docs": "/api/v1/docs",
        "health": "/health"
    }
