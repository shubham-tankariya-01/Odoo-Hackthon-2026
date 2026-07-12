from uuid import UUID, uuid4
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditCycle, AuditFinding
from app.schemas.audit import AuditCycleCreate, AuditCycleUpdate, AuditCycleProgress, AuditCycleResponse
from app.repositories.audit_repository import AuditRepository
from sqlalchemy.future import select
from app.models.asset import Asset
from app.models.allocation import Allocation


class AuditService:
    def __init__(self, session: AsyncSession):
        self.repo = AuditRepository(session)

    def _calculate_progress(self, cycle: AuditCycle) -> AuditCycleProgress:
        findings = cycle.findings or []
        return AuditCycleProgress(
            total_items=len(findings),
            verified=sum(1 for f in findings if f.status == "verified"),
            missing=sum(1 for f in findings if f.status == "missing"),
            damaged=sum(1 for f in findings if f.status == "damaged"),
            pending=sum(1 for f in findings if f.status == "pending")
        )

    def _build_response(self, cycle: AuditCycle) -> AuditCycleResponse:
        return AuditCycleResponse(
            id=cycle.id,  # type: ignore
            name=cycle.name,  # type: ignore
            scope_department_id=cycle.scope_department_id,  # type: ignore
            start_date=cycle.start_date,  # type: ignore
            end_date=cycle.end_date,  # type: ignore
            status=cycle.status,  # type: ignore
            auditor_ids=cycle.auditor_ids,  # type: ignore
            progress=self._calculate_progress(cycle)
        )

    async def create_cycle(
            self, cycle_in: AuditCycleCreate) -> AuditCycleResponse:
        new_cycle = AuditCycle(
            name=cycle_in.name,
            scope_department_id=cycle_in.scope_department_id,
            start_date=cycle_in.start_date,
            end_date=cycle_in.end_date,
            status="open",
            auditor_ids=cycle_in.auditor_ids
        )
        created_cycle = await self.repo.create_cycle(new_cycle)

        # Fetch actual assets currently allocated to the scope department
        query = (
            select(Asset.id)
            .join(Allocation, Allocation.asset_id == Asset.id)
            .where(Allocation.department_id == created_cycle.scope_department_id)
            .where(Allocation.is_active == True)
        )
        result = await self.repo.session.execute(query)
        asset_ids = result.scalars().all()

        findings = [
            AuditFinding(
                audit_cycle_id=created_cycle.id,
                asset_id=a_id,
                status="pending")
            for a_id in asset_ids
        ]
        if findings:
            await self.repo.create_findings(findings)

        # Reload cycle to get findings
        # type: ignore
        full_cycle = await self.repo.get_cycle_by_id(created_cycle.id)
        return self._build_response(full_cycle)  # type: ignore

    async def list_cycles(self) -> List[AuditCycleResponse]:
        cycles = await self.repo.get_all_cycles()
        return [self._build_response(c) for c in cycles]

    async def get_cycle(self, cycle_id: UUID) -> AuditCycleResponse:
        cycle = await self.repo.get_cycle_by_id(cycle_id)
        if not cycle:
            raise ValueError("Audit Cycle not found")
        return self._build_response(cycle)

    async def update_cycle(self, cycle_id: UUID,
                           cycle_in: AuditCycleUpdate) -> AuditCycleResponse:
        cycle = await self.repo.get_cycle_by_id(cycle_id)
        if not cycle:
            raise ValueError("Audit Cycle not found")
        if cycle.status != "open":
            raise ValueError("Cannot edit a closed audit cycle")

        if cycle_in.end_date:
            cycle.end_date = cycle_in.end_date  # type: ignore
        if cycle_in.auditor_ids is not None:
            cycle.auditor_ids = cycle_in.auditor_ids  # type: ignore

        updated = await self.repo.update_cycle(cycle)
        return self._build_response(updated)

    async def close_cycle(self, cycle_id: UUID) -> AuditCycleResponse:
        cycle = await self.repo.get_cycle_by_id(cycle_id)
        if not cycle:
            raise ValueError("Audit Cycle not found")

        # Verify no pending items
        pending_items = [f for f in cycle.findings if f.status == "pending"]
        if pending_items:
            raise ValueError("Cannot close audit with pending items")

        cycle.status = "closed"  # type: ignore
        updated = await self.repo.update_cycle(cycle)
        return self._build_response(updated)
