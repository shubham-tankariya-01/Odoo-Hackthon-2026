from pydantic import BaseModel, ConfigDict
from datetime import date
from uuid import UUID
from typing import List, Optional


class AuditCycleCreate(BaseModel):
    name: str
    scope_department_id: UUID
    start_date: date
    end_date: date
    auditor_ids: List[UUID]


class AuditCycleUpdate(BaseModel):
    end_date: Optional[date] = None
    auditor_ids: Optional[List[UUID]] = None


class AuditFindingResponse(BaseModel):
    id: UUID
    asset_id: Optional[UUID]
    status: str
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class AuditCycleProgress(BaseModel):
    total_items: int
    verified: int
    missing: int
    damaged: int
    pending: int


class AuditCycleResponse(BaseModel):
    id: UUID
    name: str
    scope_department_id: UUID
    start_date: date
    end_date: date
    status: str
    auditor_ids: List[UUID]
    progress: Optional[AuditCycleProgress] = None

    model_config = ConfigDict(from_attributes=True)
