from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.schemas.allocation import AllocationCreate, AllocationReturn, AllocationResponse
from app.schemas.common import PaginatedResponse
from app.services.allocation_service import AllocationService
from app.repositories.allocation_repo import AllocationRepository
from app.repositories.asset_repo import AssetRepository
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.utils.constants import UserRole

router = APIRouter(prefix="/allocations", tags=["Allocations"])


@router.get("", response_model=PaginatedResponse[AllocationResponse])
async def list_allocations(
    employee_id: Optional[UUID] = Query(None),
    department_id: Optional[UUID] = Query(None),
    asset_id: Optional[UUID] = Query(None),
    is_active: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List all allocations with optional filters."""
    service = AllocationService(AllocationRepository(db), AssetRepository(db))
    skip = (page - 1) * page_size
    items, total = await service.get_all(
        employee_id=employee_id,
        department_id=department_id,
        asset_id=asset_id,
        is_active=is_active,
        skip=skip,
        limit=page_size,
    )
    pages = max(1, (total + page_size - 1) // page_size)
    return {"items": items, "total": total, "page": page,
            "page_size": page_size, "pages": pages}


@router.get("/overdue", response_model=list[AllocationResponse])
async def get_overdue_allocations(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ASSET_MANAGER, UserRole.ADMIN])),
):
    """List all active allocations past their expected return date."""
    service = AllocationService(AllocationRepository(db), AssetRepository(db))
    return await service.get_overdue()


@router.get("/{alloc_id}", response_model=AllocationResponse)
async def get_allocation(
    alloc_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get single allocation detail."""
    service = AllocationService(AllocationRepository(db), AssetRepository(db))
    return await service.get_by_id(alloc_id)


@router.post("", response_model=AllocationResponse,
             status_code=status.HTTP_201_CREATED)
async def allocate_asset(
    data: AllocationCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ASSET_MANAGER, UserRole.ADMIN, UserRole.DEPARTMENT_HEAD])),
):
    """Allocate an asset to an employee. Asset must be 'available'."""
    service = AllocationService(AllocationRepository(db), AssetRepository(db))
    return await service.allocate(data, allocated_by_id=current_user.id)


@router.patch("/{alloc_id}/return", response_model=AllocationResponse)
async def return_asset(
    alloc_id: UUID,
    payload: AllocationReturn,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ASSET_MANAGER, UserRole.ADMIN])),
):
    """Mark an allocation as returned. Asset status reverts to 'available'."""
    service = AllocationService(AllocationRepository(db), AssetRepository(db))
    return await service.return_asset(alloc_id, payload)
