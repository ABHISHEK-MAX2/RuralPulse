from fastapi import APIRouter

from app.api.v1.admin import router as admin_router
from app.api.v1.auth import router as auth_router
from app.api.v1.villages import router as villages_router
from app.api.v1.watsonx import router as watsonx_router
from app.api.v1.mmus import router as mmus_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.interventions import router as interventions_router
from app.api.v1.data_quality import router as data_quality_router
from app.api.v1.reports import router as reports_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(watsonx_router, prefix="/watsonx", tags=["IBM watsonx.ai & Groq Copilot"])
api_router.include_router(villages_router, prefix="/villages", tags=["Villages Intelligence"])
api_router.include_router(mmus_router, prefix="/mmus", tags=["MMU Operations Fleet"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["Early Warning & Alerts"])
api_router.include_router(interventions_router, prefix="/interventions", tags=["Human-In-The-Loop Approvals"])
api_router.include_router(data_quality_router, prefix="/data-quality", tags=["Data Sources & Provenance Quality"])
api_router.include_router(reports_router, prefix="/reports", tags=["Executive Reports & Exports"])
api_router.include_router(admin_router, prefix="/admin", tags=["System Administration"])
