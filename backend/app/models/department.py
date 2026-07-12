from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
from sqlalchemy.orm import relationship


class Department(BaseModel):
    __tablename__ = 'departments'
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    parent_department_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("departments.id"),
        nullable=True)
    head_user_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("users.id"),
        nullable=True)
    status = Column(String, default='active', nullable=False)

    # Relationships
    users = relationship(
        'User',
        back_populates='department',
        foreign_keys='User.department_id')
    parent = relationship(
        'Department',
        remote_side='Department.id',
        foreign_keys=[parent_department_id])
    head = relationship('User', foreign_keys=[head_user_id])
