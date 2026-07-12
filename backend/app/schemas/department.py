from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from app.utils.constants import DepartmentStatus
from app.schemas.common import BaseSchema

class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    parent_department_id: Optional[UUID] = None
    head_user_id: Optional[UUID] = None
    status: DepartmentStatus = DepartmentStatus.ACTIVE

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    parent_department_id: Optional[UUID] = None
    head_user_id: Optional[UUID] = None
    status: Optional[DepartmentStatus] = None

class DepartmentChild(BaseModel):
    id: UUID
    name: str

class DepartmentResponse(BaseSchema):
    name: str
    parent_department_id: Optional[UUID] = None
    head_user_id: Optional[UUID] = None
    head_name: Optional[str] = None
    status: DepartmentStatus
    child_departments: List[DepartmentChild] = []
    member_count: int = 0
