from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceApprove,
    MaintenanceAssign,
    MaintenanceResolve,
    MaintenanceReject,
    MaintenanceResponse,
)
from app.schemas.common import PaginatedResponse
from app.services.maintenance_service import MaintenanceService
from app.repositories.maintenance_repo import MaintenanceRepository
from app.repositories.asset_repo import AssetRepository
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.utils.constants import UserRole
from app.models.maintenance import MaintenancePriority, MaintenanceStatus

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


@router.get("", response_model=PaginatedResponse[MaintenanceResponse])
async def list_maintenance(
    asset_id: Optional[UUID] = Query(None),
    raised_by_id: Optional[UUID] = Query(None),
    technician_id: Optional[UUID] = Query(None),
    status: Optional[MaintenanceStatus] = Query(None),
    priority: Optional[MaintenancePriority] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List all maintenance requests with optional filters."""
    service = MaintenanceService(
        MaintenanceRepository(db),
        AssetRepository(db))
    skip = (page - 1) * page_size
    items, total = await service.get_all(
        asset_id=asset_id,
        raised_by_id=raised_by_id,
        technician_id=technician_id,
        status=status,
        priority=priority,
        skip=skip,
        limit=page_size,
    )
    pages = max(1, (total + page_size - 1) // page_size)
    return {"items": items, "total": total, "page": page,
            "page_size": page_size, "pages": pages}


@router.get("/{request_id}", response_model=MaintenanceResponse)
async def get_maintenance(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get maintenance request detail."""
    service = MaintenanceService(
        MaintenanceRepository(db),
        AssetRepository(db))
    return await service.get_by_id(request_id)


@router.post("", response_model=MaintenanceResponse,
             status_code=status.HTTP_201_CREATED)
async def raise_maintenance(
    data: MaintenanceCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Raise a maintenance request. Does NOT change asset status —
    the asset only goes under_maintenance after approval.
    """
    service = MaintenanceService(
        MaintenanceRepository(db),
        AssetRepository(db))
    return await service.raise_request(data, raised_by_id=current_user.id)


@router.patch("/{request_id}/approve", response_model=MaintenanceResponse)
async def approve_maintenance(
    request_id: UUID,
    payload: MaintenanceApprove,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ASSET_MANAGER, UserRole.ADMIN])),
):
    """Approve a pending request — asset status flips to 'under_maintenance'."""
    service = MaintenanceService(
        MaintenanceRepository(db),
        AssetRepository(db))
    return await service.approve(request_id, payload, approved_by_id=current_user.id)


@router.patch("/{request_id}/reject", response_model=MaintenanceResponse)
async def reject_maintenance(
    request_id: UUID,
    payload: MaintenanceReject,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ASSET_MANAGER, UserRole.ADMIN])),
):
    """Reject a pending request. Asset status is not changed."""
    service = MaintenanceService(
        MaintenanceRepository(db),
        AssetRepository(db))
    return await service.reject(request_id, payload, rejected_by_id=current_user.id)


@router.patch("/{request_id}/assign", response_model=MaintenanceResponse)
async def assign_technician(
    request_id: UUID,
    payload: MaintenanceAssign,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ASSET_MANAGER, UserRole.ADMIN])),
):
    """Assign a technician to an approved request."""
    service = MaintenanceService(
        MaintenanceRepository(db),
        AssetRepository(db))
    return await service.assign(request_id, payload)


@router.patch("/{request_id}/start", response_model=MaintenanceResponse)
async def start_maintenance(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ASSET_MANAGER, UserRole.ADMIN])),
):
    """Mark maintenance as in-progress. Must be assigned first."""
    service = MaintenanceService(
        MaintenanceRepository(db),
        AssetRepository(db))
    return await service.start(request_id)


@router.patch("/{request_id}/resolve", response_model=MaintenanceResponse)
async def resolve_maintenance(
    request_id: UUID,
    payload: MaintenanceResolve,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ASSET_MANAGER, UserRole.ADMIN])),
):
    """Resolve maintenance — asset status flips back to 'available'."""
    service = MaintenanceService(
        MaintenanceRepository(db),
        AssetRepository(db))
    return await service.resolve(request_id, payload)
