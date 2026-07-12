from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from app.utils.constants import UserRole, UserStatus


class UserUpdate(BaseModel):
    name: Optional[str] = None
    department_id: Optional[UUID] = None
    status: Optional[UserStatus] = None


class UserRoleUpdate(BaseModel):
    role: UserRole
