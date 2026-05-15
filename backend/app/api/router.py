"""Main API router that includes all sub-routers."""

from fastapi import APIRouter

from app.api.generator import router as generator_router
from app.api.template import router as template_router
from app.api.api_key import router as api_key_router
from app.api.ai import router as ai_router
from app.api.history import router as history_router

api_router = APIRouter(prefix="/api")
api_router.include_router(generator_router)
api_router.include_router(template_router)
api_router.include_router(api_key_router)
api_router.include_router(ai_router)
api_router.include_router(history_router)
