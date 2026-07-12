from datetime import date, datetime, timezone
from typing import Optional, Sequence, Tuple
from uuid import UUID

from app.models.allocation import Allocation
from app.models.asset import AssetStatus
from app.repositories.allocation_repo import AllocationRepository
from app.repositories.asset_repo import AssetRepository
from app.schemas.allocation import AllocationCreate, AllocationReturn
from app.utils.exceptions import (
    ConflictException,
    NotFoundException,
    ValidationException,
)


class AllocationService:
    def __init__(self, alloc_repo: AllocationRepository,
                 asset_repo: AssetRepository):
        self.alloc_repo = alloc_repo
        self.asset_repo = asset_repo

    # ── Queries ──────────────────────────────────────

    async def get_all(
        self,
        employee_id: Optional[UUID] = None,
        department_id: Optional[UUID] = None,
        asset_id: Optional[UUID] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[Sequence[Allocation], int]:
        return await self.alloc_repo.search(
            employee_id=employee_id,
            department_id=department_id,
            asset_id=asset_id,
            is_active=is_active,
            skip=skip,
            limit=limit,
        )

    async def get_by_id(self, alloc_id: UUID) -> Allocation:
        alloc = await self.alloc_repo.get_by_id(alloc_id)
        if not alloc:
            raise NotFoundException("Allocation not found")
        return alloc

    async def get_overdue(self) -> Sequence[Allocation]:
        return await self.alloc_repo.get_overdue(today=date.today())

    # ── Mutations ─────────────────────────────────────

    async def allocate(self, data: AllocationCreate,
                       allocated_by_id: UUID) -> Allocation:
        # 1. Asset must exist
        asset = await self.asset_repo.get_by_id(data.asset_id)
        if not asset:
            raise NotFoundException("Asset not found")

        # 2. Asset must be 'available'
        if asset.current_status != AssetStatus.available:
            existing = await self.alloc_repo.get_active_by_asset(data.asset_id)
            detail = f"Asset is currently '{asset.current_status}'"
            if existing:
                detail += f" — active allocation ID: {existing.id}"
            raise ConflictException(detail)

        # 3. Create the allocation
        alloc_in = {
            **data.model_dump(),
            "allocated_by_id": allocated_by_id,
            "allocated_at": datetime.now(timezone.utc),
            "is_active": True,
        }
        allocation = await self.alloc_repo.create(alloc_in)

        # 4. Update asset status via the state-machine gate
        from app.services.asset_service import AssetService
        from app.schemas.asset import AssetStatusUpdate
        asset_service = AssetService(self.asset_repo)
        await asset_service.change_status(
            data.asset_id,
            AssetStatusUpdate(status=AssetStatus.allocated),
        )

        return allocation

    async def return_asset(
        self, alloc_id: UUID, payload: AllocationReturn
    ) -> Allocation:
        alloc = await self.get_by_id(alloc_id)

        if not alloc.is_active:
            raise ConflictException("This allocation is already closed")

        # Close the allocation
        update = {
            "is_active": False,
            "actual_return_date": datetime.now(timezone.utc),
            "return_condition": payload.return_condition,
            "return_notes": payload.return_notes,
        }
        updated = await self.alloc_repo.update(alloc, update)

        # Set asset back to 'available' via the gate
        from app.services.asset_service import AssetService
        from app.schemas.asset import AssetStatusUpdate
        asset_service = AssetService(self.asset_repo)
        await asset_service.change_status(
            alloc.asset_id,  # type: ignore
            AssetStatusUpdate(status=AssetStatus.available),
        )

        return updated
