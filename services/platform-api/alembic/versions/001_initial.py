"""Initial schema: applications, provisioning_requests, audit_events."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "applications",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=63), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("team", sa.String(length=63), nullable=False),
        sa.Column(
            "template",
            sa.Enum("WEB_API", name="application_template"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum("PENDING", "PROVISIONING", "PROVISIONED", "FAILED", name="application_status"),
            nullable=False,
        ),
        sa.Column("namespace", sa.String(length=63), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_applications_name", "applications", ["name"])
    op.create_index("ix_applications_team", "applications", ["team"])

    op.create_table(
        "provisioning_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("application_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING", "IN_PROGRESS", "COMPLETED", "FAILED", name="provisioning_status"
            ),
            nullable=False,
        ),
        sa.Column("artifacts", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["application_id"], ["applications.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_provisioning_requests_application_id", "provisioning_requests", ["application_id"])

    op.create_table(
        "audit_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("resource_type", sa.String(length=50), nullable=False),
        sa.Column("resource_id", sa.String(length=100), nullable=False),
        sa.Column("actor", sa.String(length=255), nullable=False),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audit_events_action", "audit_events", ["action"])
    op.create_index("ix_audit_events_resource_id", "audit_events", ["resource_id"])


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_table("provisioning_requests")
    op.drop_table("applications")
    op.execute("DROP TYPE IF EXISTS provisioning_status")
    op.execute("DROP TYPE IF EXISTS application_status")
    op.execute("DROP TYPE IF EXISTS application_template")
