from datetime import datetime, timezone
from typing import Optional, Sequence, Tuple
from uuid import UUID

from app.models.maintenance import MaintenanceRequest, MaintenanceStatus
from app.models.asset import AssetStatus
from app.repositories.maintenance_repo import MaintenanceRepository
from app.repositories.asset_repo import AssetRepository
from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceApprove,
    MaintenanceAssign,
    MaintenanceResolve,
    MaintenanceReject,
)
from app.utils.exceptions import (
    ConflictException,
    NotFoundException,
    ValidationException,
)


class MaintenanceService:
    def __init__(self, maint_repo: MaintenanceRepository, asset_repo: AssetRepository):
        self.maint_repo = maint_repo
        self.asset_repo = asset_repo

    # ── Queries ──────────────────────────────────────

    async def get_all(
        self,
        asset_id: Optional[UUID] = None,
        raised_by_id: Optional[UUID] = None,
        technician_id: Optional[UUID] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[Sequence[MaintenanceRequest], int]:
        return await self.maint_repo.search(
            asset_id=asset_id,
            raised_by_id=raised_by_id,
            technician_id=technician_id,
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
        )

    async def get_by_id(self, request_id: UUID) -> MaintenanceRequest:
        req = await self.maint_repo.get_by_id(request_id)
        if not req:
            raise NotFoundException("Maintenance request not found")
        return req

    # ── Mutations ─────────────────────────────────────

    async def raise_request(self, data: MaintenanceCreate, raised_by_id: UUID) -> MaintenanceRequest:
        """
        Step 1 per the README: just log the issue — do NOT change asset status yet.
        """
        asset = await self.asset_repo.get_by_id(data.asset_id)
        if not asset:
            raise NotFoundException("Asset not found")

        req_in = {
            **data.model_dump(),
            "raised_by_id": raised_by_id,
            "status": MaintenanceStatus.pending,
        }
        return await self.maint_repo.create(req_in)

    async def approve(self, request_id: UUID, payload: MaintenanceApprove, approved_by_id: UUID) -> MaintenanceRequest:
        """
        Step 3 per README: only here does the asset flip to 'under_maintenance'.
        """
        req = await self.get_by_id(request_id)

        if req.status != MaintenanceStatus.pending:
            raise ConflictException(f"Cannot approve a request in '{req.status}' status")

        # Flip asset status via the gate
        from app.services.asset_service import AssetService
        from app.schemas.asset import AssetStatusUpdate
        asset_service = AssetService(self.asset_repo)
        await asset_service.change_status(
            req.asset_id,
            AssetStatusUpdate(status=AssetStatus.under_maintenance),
        )

        return await self.maint_repo.update(req, {
            "status": MaintenanceStatus.approved,
            "approved_by_id": approved_by_id,
        })

    async def reject(self, request_id: UUID, payload: MaintenanceReject, rejected_by_id: UUID) -> MaintenanceRequest:
        req = await self.get_by_id(request_id)

        if req.status != MaintenanceStatus.pending:
            raise ConflictException(f"Cannot reject a request in '{req.status}' status")

        return await self.maint_repo.update(req, {
            "status": MaintenanceStatus.rejected,
            "resolution_notes": payload.reason,
        })

    async def assign(self, request_id: UUID, payload: MaintenanceAssign) -> MaintenanceRequest:
        req = await self.get_by_id(request_id)

        if req.status != MaintenanceStatus.approved:
            raise ConflictException(f"Can only assign a technician to an approved request, current status: '{req.status}'")

        return await self.maint_repo.update(req, {
            "status": MaintenanceStatus.assigned,
            "technician_id": payload.technician_id,
        })

    async def start(self, request_id: UUID) -> MaintenanceRequest:
        req = await self.get_by_id(request_id)

        if req.status != MaintenanceStatus.assigned:
            raise ConflictException(f"Cannot start work on a request in '{req.status}' status — must be assigned first")

        return await self.maint_repo.update(req, {"status": MaintenanceStatus.in_progress})

    async def resolve(self, request_id: UUID, payload: MaintenanceResolve) -> MaintenanceRequest:
        """
        Step 5 per README: only here does the asset flip back to 'available'.
        """
        req = await self.get_by_id(request_id)

        if req.status != MaintenanceStatus.in_progress:
            raise ConflictException(f"Cannot resolve a request in '{req.status}' status — must be in_progress first")

        # Flip asset back to available via the gate
        from app.services.asset_service import AssetService
        from app.schemas.asset import AssetStatusUpdate
        asset_service = AssetService(self.asset_repo)
        await asset_service.change_status(
            req.asset_id,
            AssetStatusUpdate(status=AssetStatus.available),
        )

        return await self.maint_repo.update(req, {
            "status": MaintenanceStatus.resolved,
            "resolution_notes": payload.resolution_notes,
            "resolved_at": datetime.now(timezone.utc),
        })
