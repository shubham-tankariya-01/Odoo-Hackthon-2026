from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.utils.constants import DepartmentStatus

class Department(BaseModel):
    __tablename__ = "departments"

    name = Column(String, unique=True, index=True, nullable=False)
    parent_department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    head_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status = Column(String, default=DepartmentStatus.ACTIVE, nullable=False)
