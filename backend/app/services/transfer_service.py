from datetime import datetime, timezone
from typing import Optional, Sequence, Tuple
from uuid import UUID

from app.models.transfer import Transfer, TransferStatus
from app.repositories.transfer_repo import TransferRepository
from app.repositories.allocation_repo import AllocationRepository
from app.repositories.asset_repo import AssetRepository
from app.schemas.transfer import TransferCreate
from app.schemas.allocation import AllocationCreate, AllocationReturn
from app.services.allocation_service import AllocationService
from app.utils.exceptions import (
    ConflictException,
    NotFoundException,
    ForbiddenException,
)


class TransferService:
    def __init__(
        self,
        transfer_repo: TransferRepository,
        alloc_repo: AllocationRepository,
        asset_repo: AssetRepository,
    ):
        self.transfer_repo = transfer_repo
        self.alloc_repo = alloc_repo
        self.asset_repo = asset_repo

    # ── Queries ──────────────────────────────────────

    async def get_all(
        self,
        asset_id: Optional[UUID] = None,
        from_employee_id: Optional[UUID] = None,
        to_employee_id: Optional[UUID] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[Sequence[Transfer], int]:
        return await self.transfer_repo.search(
            asset_id=asset_id,
            from_employee_id=from_employee_id,
            to_employee_id=to_employee_id,
            status=status,
            skip=skip,
            limit=limit,
        )

    async def get_by_id(self, transfer_id: UUID) -> Transfer:
        transfer = await self.transfer_repo.get_by_id(transfer_id)
        if not transfer:
            raise NotFoundException("Transfer request not found")
        return transfer

    # ── Mutations ─────────────────────────────────────

    async def request_transfer(
        self, data: TransferCreate, requested_by_id: UUID
    ) -> Transfer:
        """
        Step 3.2: Only allowed if the asset is currently allocated to someone.
        """
        # Find the active allocation of this asset
        active_alloc = await self.alloc_repo.get_active_by_asset(data.asset_id)
        if not active_alloc:
            raise ConflictException(
                "You cannot request a transfer for an asset that is not currently allocated to anyone"
            )

        if active_alloc.employee_id == data.to_employee_id:
            raise ConflictException(
                "Asset is already allocated to the destination user"
            )

        # Create transfer request
        transfer_in = {
            **data.model_dump(),
            "from_employee_id": active_alloc.employee_id,
            "requested_by_id": requested_by_id,
            "status": TransferStatus.requested,
        }
        return await self.transfer_repo.create(transfer_in)

    async def approve(self, transfer_id: UUID, approved_by_id: UUID) -> Transfer:
        """
        Step 3.3: Close the old allocation and open a new one for the receiver.
        Reuses the existing allocation service logic to maintain status check integrity.
        """
        transfer = await self.get_by_id(transfer_id)

        if transfer.status != TransferStatus.requested:
            raise ConflictException(
                f"Cannot approve transfer request in '{transfer.status}' status"
            )

        # 1. Check if the active allocation still belongs to the 'from_employee'
        active_alloc = await self.alloc_repo.get_active_by_asset(transfer.asset_id)
        if not active_alloc or active_alloc.employee_id != transfer.from_employee_id:
            raise ConflictException(
                "The source allocation has changed. This transfer request is no longer valid."
            )

        # 2. Return the asset from the current holder (closes old allocation)
        # Reuses the return_asset flow from Step 2
        alloc_service = AllocationService(self.alloc_repo, self.asset_repo)
        await alloc_service.return_asset(
            active_alloc.id,
            AllocationReturn(
                return_condition="Good",
                return_notes=f"Auto-returned during Transfer approval ID: {transfer.id}",
            ),
        )

        # 3. Create the new allocation to the destination holder
        # Reuses the allocate flow from Step 2
        await alloc_service.allocate(
            AllocationCreate(
                asset_id=transfer.asset_id,
                employee_id=transfer.to_employee_id,
                department_id=active_alloc.department_id,  # Preserve department if any
                expected_return_date=active_alloc.expected_return_date,
            ),
            allocated_by_id=approved_by_id,
        )

        # 4. Mark transfer request as completed
        return await self.transfer_repo.update(
            transfer,
            {
                "status": TransferStatus.completed,
                "approved_by_id": approved_by_id,
                "resolved_at": datetime.now(timezone.utc),
            },
        )

    async def reject(self, transfer_id: UUID, approved_by_id: UUID) -> Transfer:
        transfer = await self.get_by_id(transfer_id)

        if transfer.status != TransferStatus.requested:
            raise ConflictException(
                f"Cannot reject transfer request in '{transfer.status}' status"
            )

        return await self.transfer_repo.update(
            transfer,
            {
                "status": TransferStatus.rejected,
                "approved_by_id": approved_by_id,
                "resolved_at": datetime.now(timezone.utc),
            },
        )

    async def cancel(self, transfer_id: UUID, user_id: UUID) -> Transfer:
        """
        Step 3.4: Cancel can only work for the person who originally made the request.
        """
        transfer = await self.get_by_id(transfer_id)

        if transfer.status != TransferStatus.requested:
            raise ConflictException(
                f"Cannot cancel transfer request in '{transfer.status}' status"
            )

        if transfer.requested_by_id != user_id:
            raise ForbiddenException(
                "Only the requester is allowed to cancel this transfer request"
            )

        return await self.transfer_repo.update(
            transfer,
            {
                "status": TransferStatus.cancelled,
                "resolved_at": datetime.now(timezone.utc),
            },
        )
