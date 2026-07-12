from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.schemas.common import PaginatedResponse
from app.controllers.department_controller import DepartmentController
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.utils.constants import UserRole

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("", response_model=PaginatedResponse[DepartmentResponse])
async def list_departments(
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await DepartmentController.get_all(db, status, page, page_size)


@router.get("/{dept_id}", response_model=DepartmentResponse)
async def get_department(
    dept_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await DepartmentController.get_by_id(dept_id, db)


@router.post("", response_model=DepartmentResponse,
             status_code=status.HTTP_201_CREATED)
async def create_department(
    data: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role([UserRole.ADMIN]))
):
    return await DepartmentController.create(data, db)


@router.patch("/{dept_id}", response_model=DepartmentResponse)
async def update_department(
    dept_id: UUID,
    data: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role([UserRole.ADMIN]))
):
    return await DepartmentController.update(dept_id, data, db)
