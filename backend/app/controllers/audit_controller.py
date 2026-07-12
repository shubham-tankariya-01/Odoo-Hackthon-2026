from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas.audit import AuditCycleCreate, AuditCycleUpdate
from app.services.audit_service import AuditService

class AuditController:
    @staticmethod
    async def create_cycle(cycle_in: AuditCycleCreate, db: AsyncSession):
        service = AuditService(db)
        return await service.create_cycle(cycle_in)

    @staticmethod
    async def get_cycles(db: AsyncSession):
        service = AuditService(db)
        return await service.list_cycles()

    @staticmethod
    async def get_cycle(cycle_id: UUID, db: AsyncSession):
        service = AuditService(db)
        try:
            return await service.get_cycle(cycle_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    async def update_cycle(cycle_id: UUID, cycle_in: AuditCycleUpdate, db: AsyncSession):
        service = AuditService(db)
        try:
            return await service.update_cycle(cycle_id, cycle_in)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def close_cycle(cycle_id: UUID, db: AsyncSession):
        service = AuditService(db)
        try:
            return await service.close_cycle(cycle_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
