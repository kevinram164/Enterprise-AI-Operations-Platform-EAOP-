from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.models import Application, ApplicationStatus, AuditEvent
from app.schemas import (
    ApplicationCreate,
    ApplicationListResponse,
    ApplicationResponse,
    ArtifactsResponse,
    ProvisioningRequestResponse,
)
from app.services.events import publish_event
from app.services.provisioning import ProvisioningError, get_latest_artifacts, provision_application

router = APIRouter(prefix="/applications", tags=["applications"])
settings = get_settings()


def _build_namespace(team: str, name: str) -> str:
    return f"team-{team}-{name}"


@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    payload: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
) -> Application:
    existing = await db.scalar(select(Application).where(Application.name == payload.name))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Application '{payload.name}' already exists",
        )

    application = Application(
        name=payload.name,
        display_name=payload.display_name,
        team=payload.team,
        template=payload.template,
        namespace=_build_namespace(payload.team, payload.name),
        description=payload.description,
        status=ApplicationStatus.PENDING,
    )
    db.add(application)
    await db.flush()

    db.add(
        AuditEvent(
            action="application.created",
            resource_type="application",
            resource_id=str(application.id),
            details={"name": application.name, "team": application.team},
        )
    )

    await db.refresh(application)

    await publish_event(
        "application.created",
        {
            "application_id": str(application.id),
            "name": application.name,
            "team": application.team,
            "namespace": application.namespace,
        },
    )

    return application


@router.get("", response_model=ApplicationListResponse)
async def list_applications(
    team: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> ApplicationListResponse:
    query = select(Application).order_by(Application.created_at.desc())
    if team:
        query = query.where(Application.team == team)

    result = await db.execute(query)
    items = result.scalars().all()
    return ApplicationListResponse(items=items, total=len(items))


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Application:
    application = await db.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application


@router.post(
    "/{application_id}/provision",
    response_model=ProvisioningRequestResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def provision_app(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ProvisioningRequestResponse:
    try:
        request = await provision_application(db, application_id)
    except ProvisioningError as exc:
        message = str(exc)
        if message == "Application not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message) from exc
        if "already" in message:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message) from exc
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message) from exc
    return request


@router.get("/{application_id}/artifacts", response_model=ArtifactsResponse)
async def get_artifacts(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ArtifactsResponse:
    application = await db.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    artifacts = await get_latest_artifacts(db, application_id)
    if not artifacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No artifacts found — provision the application first",
        )

    return ArtifactsResponse(application_id=application_id, artifacts=artifacts)
