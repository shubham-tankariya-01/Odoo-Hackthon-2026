from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime

class ActivityLogCreate(BaseModel):
    actor_user_id: Optional[UUID] = None
    recipient_user_id: Optional[UUID] = None
    action: str
    entity_type: str

class ActivityLogResponse(BaseModel):
    id: UUID
    actor_user_id: Optional[UUID]
    recipient_user_id: Optional[UUID]
    action: str
    entity_type: str
    is_read: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
