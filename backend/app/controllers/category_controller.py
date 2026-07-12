from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService
from app.repositories.category_repository import CategoryRepository
from app.utils.responses import paginated_response

class CategoryController:
    @staticmethod
    async def get_all(db: AsyncSession, page: int = 1, page_size: int = 20):
        service = CategoryService(CategoryRepository(db))
        skip = (page - 1) * page_size
        items, total = await service.get_all(skip=skip, limit=page_size)
        return paginated_response(items, total, page, page_size)

    @staticmethod
    async def get_by_id(cat_id: UUID, db: AsyncSession):
        service = CategoryService(CategoryRepository(db))
        return await service.get_by_id(cat_id)

    @staticmethod
    async def create(data: CategoryCreate, db: AsyncSession):
        service = CategoryService(CategoryRepository(db))
        cat = await service.create(data)
        return await service.get_by_id(cat.id)

    @staticmethod
    async def update(cat_id: UUID, data: CategoryUpdate, db: AsyncSession):
        service = CategoryService(CategoryRepository(db))
        cat = await service.update(cat_id, data)
        return await service.get_by_id(cat.id)
        
    @staticmethod
    async def delete(cat_id: UUID, db: AsyncSession):
        service = CategoryService(CategoryRepository(db))
        await service.delete(cat_id)
        return {"message": "Category deleted successfully"}
