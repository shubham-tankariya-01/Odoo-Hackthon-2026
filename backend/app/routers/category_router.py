from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.controllers.category_controller import CategoryController
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.utils.constants import UserRole

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=PaginatedResponse[CategoryResponse])
async def list_categories(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await CategoryController.get_all(db, page, page_size)


@router.get("/{cat_id}", response_model=CategoryResponse)
async def get_category(
    cat_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await CategoryController.get_by_id(cat_id, db)


@router.post("", response_model=CategoryResponse,
             status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ADMIN, UserRole.ASSET_MANAGER]))
):
    return await CategoryController.create(data, db)


@router.patch("/{cat_id}", response_model=CategoryResponse)
async def update_category(
    cat_id: UUID,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ADMIN, UserRole.ASSET_MANAGER]))
):
    return await CategoryController.update(cat_id, data, db)


@router.delete("/{cat_id}", response_model=MessageResponse)
async def delete_category(
    cat_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role([UserRole.ADMIN]))
):
    return await CategoryController.delete(cat_id, db)
