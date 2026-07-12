from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.services.department_service import DepartmentService
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.utils.responses import paginated_response

class DepartmentController:
    @staticmethod
    async def get_all(db: AsyncSession, status: Optional[str] = None, page: int = 1, page_size: int = 20):
        service = DepartmentService(DepartmentRepository(db), UserRepository(db))
        skip = (page - 1) * page_size
        items, total = await service.get_all(status=status, skip=skip, limit=page_size)
        return paginated_response(items, total, page, page_size)

    @staticmethod
    async def get_by_id(dept_id: UUID, db: AsyncSession):
        service = DepartmentService(DepartmentRepository(db), UserRepository(db))
        return await service.get_by_id(dept_id)

    @staticmethod
    async def create(data: DepartmentCreate, db: AsyncSession):
        service = DepartmentService(DepartmentRepository(db), UserRepository(db))
        dept = await service.create(data)
        # Refetch for rich response
        return await service.get_by_id(dept.id)

    @staticmethod
    async def update(dept_id: UUID, data: DepartmentUpdate, db: AsyncSession):
        service = DepartmentService(DepartmentRepository(db), UserRepository(db))
        dept = await service.update(dept_id, data)
        # Refetch for rich response
        return await service.get_by_id(dept.id)
