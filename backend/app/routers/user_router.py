from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
from app.schemas.user import UserUpdate, UserRoleUpdate
from app.schemas.auth import UserProfile
from app.schemas.common import PaginatedResponse
from app.controllers.user_controller import UserController
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.utils.constants import UserRole

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=PaginatedResponse[UserProfile])
async def list_users(
    department_id: Optional[UUID] = None,
    role: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ADMIN, UserRole.DEPARTMENT_HEAD, UserRole.ASSET_MANAGER]))
):
    return await UserController.get_all(db, department_id, role, status, page, page_size)


@router.get("/{user_id}", response_model=UserProfile)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(
        [UserRole.ADMIN, UserRole.DEPARTMENT_HEAD]))
):
    return await UserController.get_by_id(user_id, db)


@router.patch("/{user_id}", response_model=UserProfile)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role([UserRole.ADMIN]))
):
    return await UserController.update(user_id, data, db)


@router.post("/{user_id}/promote", response_model=UserProfile)
async def promote_user(
    user_id: UUID,
    data: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role([UserRole.ADMIN]))
):
    return await UserController.promote(user_id, data, db, current_user.id)
