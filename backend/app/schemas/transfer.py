from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.schemas.common import BaseSchema
from app.models.transfer import TransferStatus


class TransferCreate(BaseModel):
    asset_id: UUID
    to_employee_id: UUID
    reason: str = Field(..., min_length=5)


class TransferResponse(BaseSchema):
    asset_id: UUID
    from_employee_id: UUID
    to_employee_id: UUID
    status: TransferStatus
    requested_by_id: UUID
    approved_by_id: Optional[UUID] = None
    reason: str
    resolved_at: Optional[datetime] = None
