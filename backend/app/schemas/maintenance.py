from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.schemas.common import BaseSchema
from app.models.maintenance import MaintenancePriority, MaintenanceStatus


class MaintenanceCreate(BaseModel):
    asset_id: UUID
    description: str = Field(..., min_length=5)
    priority: MaintenancePriority = MaintenancePriority.medium
    photo_url: Optional[str] = None


class MaintenanceApprove(BaseModel):
    notes: Optional[str] = None


class MaintenanceAssign(BaseModel):
    technician_id: UUID


class MaintenanceResolve(BaseModel):
    resolution_notes: str = Field(..., min_length=5)


class MaintenanceReject(BaseModel):
    reason: Optional[str] = None


class MaintenanceResponse(BaseSchema):
    asset_id: UUID
    raised_by_id: UUID
    description: str
    priority: MaintenancePriority
    status: MaintenanceStatus
    approved_by_id: Optional[UUID] = None
    technician_id: Optional[UUID] = None
    resolution_notes: Optional[str] = None
    photo_url: Optional[str] = None
    resolved_at: Optional[datetime] = None
