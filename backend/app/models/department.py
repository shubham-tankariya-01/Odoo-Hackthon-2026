from sqlalchemy import Column, String, Boolean
from app.models.base import BaseModel
from sqlalchemy.orm import relationship

class Department(BaseModel):
    __tablename__ = 'departments'
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default='active', nullable=False)
    users = relationship('User', back_populates='department')
