from fastapi import APIRouter

from app.api.v1 import applications, audit, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(applications.router, prefix="/v1")
api_router.include_router(audit.router, prefix="/v1")
