from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.schemas.asset import AssetCreate, AssetUpdate, AssetStatusUpdate, AssetResponse
from app.schemas.common import PaginatedResponse
from app.services.asset_service import AssetService
from app.repositories.asset_repo import AssetRepository
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.utils.constants import UserRole
from app.models.asset import AssetStatus

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("", response_model=PaginatedResponse[AssetResponse])
async def list_assets(
    asset_tag: Optional[str] = Query(None),
    serial_number: Optional[str] = Query(None),
    category_id: Optional[UUID] = Query(None),
    current_status: Optional[AssetStatus] = Query(None),
    is_bookable: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List all assets with optional filters and search."""
    service = AssetService(AssetRepository(db))
    skip = (page - 1) * page_size
    items, total = await service.get_all(
        asset_tag=asset_tag,
        serial_number=serial_number,
        category_id=category_id,
        current_status=current_status,
        is_bookable=is_bookable,
        search=search,
        skip=skip,
        limit=page_size,
    )
    pages = max(1, (total + page_size - 1) // page_size)
    return {"items": items, "total": total, "page": page,
            "page_size": page_size, "pages": pages}


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get full asset detail by ID."""
    service = AssetService(AssetRepository(db))
    return await service.get_by_id(asset_id)


@router.post("", response_model=AssetResponse,
             status_code=status.HTTP_201_CREATED)
async def create_asset(
    data: AssetCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ASSET_MANAGER, UserRole.ADMIN])),
):
    """Register a new asset. asset_tag is auto-generated (AF-XXXX)."""
    service = AssetService(AssetRepository(db))
    return await service.create(data)


@router.patch("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: UUID,
    data: AssetUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ASSET_MANAGER, UserRole.ADMIN])),
):
    """Update asset details (name, serial, category, bookable, custom_fields)."""
    service = AssetService(AssetRepository(db))
    return await service.update(asset_id, data)


@router.patch("/{asset_id}/status", response_model=AssetResponse)
async def change_asset_status(
    asset_id: UUID,
    payload: AssetStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ASSET_MANAGER, UserRole.ADMIN])),
):
    """Change asset status — validated against the state machine."""
    service = AssetService(AssetRepository(db))
    return await service.change_status(asset_id, payload)


@router.delete("/{asset_id}", response_model=AssetResponse)
async def dispose_asset(
    asset_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role([UserRole.ADMIN])),
):
    """Soft-delete: sets status to 'disposed'. Only admin can do this."""
    service = AssetService(AssetRepository(db))
    return await service.dispose(asset_id)
