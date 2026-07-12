from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.schemas.activity_log import ActivityLogResponse
from app.controllers.activity_log_controller import ActivityLogController
from app.dependencies.database import get_db

from app.dependencies.auth import get_current_user

router = APIRouter(tags=["Activity Logs & Notifications"])


@router.get("/activity", response_model=List[ActivityLogResponse])
async def get_global_activity_log(db: AsyncSession = Depends(get_db)):
    """Admin-only audit trail."""
    return await ActivityLogController.get_audit_trail(db)


@router.get("/notifications", response_model=List[ActivityLogResponse])
async def get_user_notifications(current_user=Depends(
        get_current_user), db: AsyncSession = Depends(get_db)):
    """User-facing notifications."""
    return await ActivityLogController.get_notifications(current_user.id, db)


@router.patch("/notifications/{notification_id}/read",
              response_model=ActivityLogResponse)
async def mark_notification_read(notification_id: UUID, current_user=Depends(
        get_current_user), db: AsyncSession = Depends(get_db)):
    """Mark a specific notification as read."""
    return await ActivityLogController.mark_notification_read(notification_id, current_user.id, db)
