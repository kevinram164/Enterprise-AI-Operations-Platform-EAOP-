from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.models import (
    Application,
    ApplicationStatus,
    AuditEvent,
    ProvisioningRequest,
    ProvisioningStatus,
)
from app.services.events import publish_event
from app.services.golden_path import GoldenPathEngine, build_context

settings = get_settings()
engine = GoldenPathEngine()


class ProvisioningError(Exception):
    pass


async def provision_application(db: AsyncSession, application_id: UUID) -> ProvisioningRequest:
    application = await db.scalar(
        select(Application)
        .where(Application.id == application_id)
        .options(selectinload(Application.provisioning_requests))
    )
    if not application:
        raise ProvisioningError("Application not found")

    if application.status == ApplicationStatus.PROVISIONING:
        raise ProvisioningError("Application is already being provisioned")

    if application.status == ApplicationStatus.PROVISIONED:
        raise ProvisioningError("Application is already provisioned")

    application.status = ApplicationStatus.PROVISIONING
    request = ProvisioningRequest(
        application_id=application.id,
        status=ProvisioningStatus.IN_PROGRESS,
    )
    db.add(request)
    await db.flush()

    try:
        context = build_context(
            app_name=application.name,
            display_name=application.display_name,
            team=application.team,
            namespace=application.namespace,
            template=application.template.value,
            ocp_base_domain=settings.ocp_base_domain,
            description=application.description,
        )
        artifacts = engine.render(application.template.value, context)

        request.artifacts = artifacts
        request.status = ProvisioningStatus.COMPLETED
        request.completed_at = datetime.now(UTC)
        application.status = ApplicationStatus.PROVISIONED

        db.add(
            AuditEvent(
                action="application.provisioned",
                resource_type="application",
                resource_id=str(application.id),
                details={
                    "name": application.name,
                    "namespace": application.namespace,
                    "artifact_count": len(artifacts),
                },
            )
        )

        await publish_event(
            "application.provisioned",
            {
                "application_id": str(application.id),
                "name": application.name,
                "team": application.team,
                "namespace": application.namespace,
            },
        )
    except Exception as exc:
        request.status = ProvisioningStatus.FAILED
        request.error_message = str(exc)
        request.completed_at = datetime.now(UTC)
        application.status = ApplicationStatus.FAILED

        db.add(
            AuditEvent(
                action="application.provision_failed",
                resource_type="application",
                resource_id=str(application.id),
                details={"error": str(exc)},
            )
        )

        await publish_event(
            "application.failed",
            {
                "application_id": str(application.id),
                "name": application.name,
                "error": str(exc),
            },
        )
        raise ProvisioningError(str(exc)) from exc

    await db.refresh(request)
    return request


async def get_latest_artifacts(db: AsyncSession, application_id: UUID) -> dict[str, str] | None:
    result = await db.scalar(
        select(ProvisioningRequest)
        .where(
            ProvisioningRequest.application_id == application_id,
            ProvisioningRequest.status == ProvisioningStatus.COMPLETED,
        )
        .order_by(ProvisioningRequest.completed_at.desc())
        .limit(1)
    )
    if not result or not result.artifacts:
        return None
    return result.artifacts
