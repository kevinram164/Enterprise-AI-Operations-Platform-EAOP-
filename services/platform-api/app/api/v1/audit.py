from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import AuditEvent
from app.schemas import AuditEventResponse, AuditListResponse

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("", response_model=AuditListResponse)
async def list_audit_events(
    resource_id: str | None = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
) -> AuditListResponse:
    query = select(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(min(limit, 200))
    if resource_id:
        query = query.where(AuditEvent.resource_id == resource_id)

    result = await db.execute(query)
    items = result.scalars().all()
    return AuditListResponse(items=items, total=len(items))
