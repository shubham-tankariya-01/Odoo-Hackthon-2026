from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.schemas.transfer import TransferCreate, TransferResponse
from app.schemas.common import PaginatedResponse
from app.services.transfer_service import TransferService
from app.repositories.transfer_repo import TransferRepository
from app.repositories.allocation_repo import AllocationRepository
from app.repositories.asset_repo import AssetRepository
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.utils.constants import UserRole
from app.models.transfer import TransferStatus

router = APIRouter(prefix="/transfers", tags=["Transfers"])


@router.get("", response_model=PaginatedResponse[TransferResponse])
async def list_transfers(
    asset_id: Optional[UUID] = Query(None),
    from_employee_id: Optional[UUID] = Query(None),
    to_employee_id: Optional[UUID] = Query(None),
    status: Optional[TransferStatus] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List transfer requests with optional filters."""
    service = TransferService(TransferRepository(db), AllocationRepository(db), AssetRepository(db))
    skip = (page - 1) * page_size
    items, total = await service.get_all(
        asset_id=asset_id,
        from_employee_id=from_employee_id,
        to_employee_id=to_employee_id,
        status=status,
        skip=skip,
        limit=page_size,
    )
    pages = max(1, (total + page_size - 1) // page_size)
    return {"items": items, "total": total, "page": page, "page_size": page_size, "pages": pages}


@router.get("/{transfer_id}", response_model=TransferResponse)
async def get_transfer(
    transfer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get transfer request details by ID."""
    service = TransferService(TransferRepository(db), AllocationRepository(db), AssetRepository(db))
    return await service.get_by_id(transfer_id)


@router.post("", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
async def request_transfer(
    data: TransferCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Request an asset transfer.
    Can only be done if the asset is currently allocated.
    """
    service = TransferService(TransferRepository(db), AllocationRepository(db), AssetRepository(db))
    return await service.request_transfer(data, requested_by_id=current_user.id)


@router.patch("/{transfer_id}/approve", response_model=TransferResponse)
async def approve_transfer(
    transfer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role([UserRole.ASSET_MANAGER, UserRole.ADMIN, UserRole.DEPARTMENT_HEAD])),
):
    """
    Approve transfer request.
    Closes the old allocation and opens a new allocation for the destination user.
    """
    service = TransferService(TransferRepository(db), AllocationRepository(db), AssetRepository(db))
    return await service.approve(transfer_id, approved_by_id=current_user.id)


@router.patch("/{transfer_id}/reject", response_model=TransferResponse)
async def reject_transfer(
    transfer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role([UserRole.ASSET_MANAGER, UserRole.ADMIN, UserRole.DEPARTMENT_HEAD])),
):
    """Reject transfer request."""
    service = TransferService(TransferRepository(db), AllocationRepository(db), AssetRepository(db))
    return await service.reject(transfer_id, approved_by_id=current_user.id)


@router.patch("/{transfer_id}/cancel", response_model=TransferResponse)
async def cancel_transfer(
    transfer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Cancel transfer request. Can only be done by the original requester."""
    service = TransferService(TransferRepository(db), AllocationRepository(db), AssetRepository(db))
    return await service.cancel(transfer_id, user_id=current_user.id)
