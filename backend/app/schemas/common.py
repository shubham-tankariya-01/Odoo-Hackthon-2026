from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, List, Optional, Any
from uuid import UUID
from datetime import datetime

T = TypeVar('T')

class MessageResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str
    errors: Optional[List[Any]] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int

class BaseSchema(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
