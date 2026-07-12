from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from uuid import UUID
from app.models.audit import AuditCycle, AuditFinding


class AuditRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_cycle(self, cycle: AuditCycle) -> AuditCycle:
        self.session.add(cycle)
        await self.session.commit()
        await self.session.refresh(cycle)
        return cycle

    async def create_findings(self, findings: List[AuditFinding]):
        self.session.add_all(findings)
        await self.session.commit()

    async def get_all_cycles(self) -> List[AuditCycle]:
        result = await self.session.execute(
            select(AuditCycle).options(selectinload(AuditCycle.findings))
        )
        return list(result.scalars().all())

    async def get_cycle_by_id(self, cycle_id: UUID) -> Optional[AuditCycle]:
        result = await self.session.execute(
            select(AuditCycle)
            .options(selectinload(AuditCycle.findings))
            .where(AuditCycle.id == cycle_id)
        )
        return result.scalars().first()

    async def update_cycle(self, cycle: AuditCycle) -> AuditCycle:
        await self.session.commit()
        await self.session.refresh(cycle)
        return cycle
