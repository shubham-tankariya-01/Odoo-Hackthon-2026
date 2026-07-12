from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity_log import ActivityLog
from app.schemas.activity_log import ActivityLogCreate
from app.repositories.activity_log_repository import ActivityLogRepository


class ActivityLogService:
    def __init__(self, session: AsyncSession):
        self.repo = ActivityLogRepository(session)

    async def log_action(self, log_in: ActivityLogCreate) -> ActivityLog:
        new_log = ActivityLog(
            actor_user_id=log_in.actor_user_id,
            recipient_user_id=log_in.recipient_user_id,
            action=log_in.action,
            entity_type=log_in.entity_type,
            is_read=False
        )
        return await self.repo.create(new_log)

    async def get_audit_trail(self) -> List[ActivityLog]:
        return await self.repo.get_all()

    async def get_user_notifications(self, user_id: UUID) -> List[ActivityLog]:
        return await self.repo.get_by_recipient(user_id)

    async def mark_notification_read(
            self, notification_id: UUID, user_id: UUID) -> ActivityLog:
        log = await self.repo.get_by_id(notification_id)
        if not log:
            raise ValueError("Notification not found")
        if log.recipient_user_id != user_id:
            raise PermissionError("Cannot modify another user's notification")

        return await self.repo.mark_as_read(log)
