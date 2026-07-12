from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from app.schemas.common import BaseSchema
from app.models.allocation import AllocationStatus


class AllocationCreate(BaseModel):
    asset_id: UUID
    employee_id: UUID
    department_id: Optional[UUID] = None
    expected_return_date: Optional[date] = None


class AllocationReturn(BaseModel):
    return_condition: Optional[str] = Field(None, max_length=100)
    return_notes: Optional[str] = None


class AllocationResponse(BaseSchema):
    asset_id: UUID
    employee_id: UUID
    department_id: Optional[UUID] = None
    allocated_by_id: Optional[UUID] = None
    allocated_at: Optional[datetime] = None
    expected_return_date: Optional[date] = None
    actual_return_date: Optional[datetime] = None
    return_condition: Optional[str] = None
    return_notes: Optional[str] = None
    is_active: bool
