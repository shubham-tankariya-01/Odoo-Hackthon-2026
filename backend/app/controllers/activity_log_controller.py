from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.services.activity_log_service import ActivityLogService


class ActivityLogController:
    @staticmethod
    async def get_audit_trail(db: AsyncSession):
        service = ActivityLogService(db)
        return await service.get_audit_trail()

    @staticmethod
    async def get_notifications(user_id: UUID, db: AsyncSession):
        service = ActivityLogService(db)
        return await service.get_user_notifications(user_id)

    @staticmethod
    async def mark_notification_read(
            notification_id: UUID, user_id: UUID, db: AsyncSession):
        service = ActivityLogService(db)
        try:
            return await service.mark_notification_read(notification_id, user_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
