import redis.asyncio as aioredis
from fastapi import APIRouter
from sqlalchemy import text

from app.config import get_settings
from app.database import async_session_factory
from app.schemas import HealthResponse

router = APIRouter(tags=["health"])
settings = get_settings()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    services: dict[str, str] = {"api": "ok"}

    try:
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))
        services["postgres"] = "ok"
    except Exception:
        services["postgres"] = "error"

    try:
        client = aioredis.from_url(settings.redis_url)
        await client.ping()
        await client.aclose()
        services["redis"] = "ok"
    except Exception:
        services["redis"] = "error"

    overall = "ok" if all(v == "ok" for v in services.values()) else "degraded"
    return HealthResponse(status=overall, version=settings.app_version, services=services)
