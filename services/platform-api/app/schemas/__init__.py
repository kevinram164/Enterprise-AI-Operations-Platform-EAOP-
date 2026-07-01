from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models import ApplicationStatus, ApplicationTemplate, ProvisioningStatus


class ApplicationCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=63, pattern=r"^[a-z][a-z0-9-]*$")
    display_name: str = Field(..., min_length=2, max_length=255)
    team: str = Field(..., min_length=2, max_length=63, pattern=r"^[a-z][a-z0-9-]*$")
    template: ApplicationTemplate = ApplicationTemplate.WEB_API
    description: str | None = None


class ApplicationResponse(BaseModel):
    id: UUID
    name: str
    display_name: str
    team: str
    template: ApplicationTemplate
    status: ApplicationStatus
    namespace: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApplicationListResponse(BaseModel):
    items: list[ApplicationResponse]
    total: int


class ProvisioningRequestResponse(BaseModel):
    id: UUID
    application_id: UUID
    status: ProvisioningStatus
    artifacts: dict | None
    error_message: str | None
    created_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class HealthResponse(BaseModel):
    status: str
    version: str
    services: dict[str, str]


class ArtifactsResponse(BaseModel):
    application_id: UUID
    artifacts: dict[str, str]


class AuditEventResponse(BaseModel):
    id: UUID
    action: str
    resource_type: str
    resource_id: str
    actor: str
    details: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AuditListResponse(BaseModel):
    items: list[AuditEventResponse]
    total: int
