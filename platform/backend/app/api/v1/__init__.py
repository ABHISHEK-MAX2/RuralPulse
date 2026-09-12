from fastapi import APIRouter

from app.api.v1.admin import router as admin_router
from app.api.v1.auth import router as auth_router
from app.api.v1.villages import router as villages_router
from app.api.v1.watsonx import router as watsonx_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(watsonx_router, prefix="/watsonx", tags=["IBM watsonx.ai & Groq Copilot"])
api_router.include_router(villages_router, prefix="/villages", tags=["Villages Intelligence"])
api_router.include_router(admin_router, prefix="/admin", tags=["System Administration"])
