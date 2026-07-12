from typing import List, Tuple
from uuid import UUID
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.asset_category import AssetCategory
from app.repositories.category_repository import CategoryRepository
from app.utils.exceptions import ConflictException, NotFoundException, ValidationException

class CategoryService:
    def __init__(self, cat_repo: CategoryRepository):
        self.cat_repo = cat_repo

    async def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List[dict], int]:
        categories = await self.cat_repo.get_all(skip, limit)
        total = len(categories)
        result = []
        for cat in categories:
            # Hardcode asset_count to 0 for now as assets table isn't built yet
            asset_count = 0
            result.append({
                "id": cat.id,
                "name": cat.name,
                "description": cat.description,
                "asset_count": asset_count,
                "created_at": cat.created_at,
                "updated_at": cat.updated_at
            })
        return result, total

    async def get_by_id(self, cat_id: UUID) -> dict:
        cat = await self.cat_repo.get_by_id(cat_id)
        if not cat:
            raise NotFoundException("Category not found")
        return {
            "id": cat.id,
            "name": cat.name,
            "description": cat.description,
            "asset_count": 0,
            "created_at": cat.created_at,
            "updated_at": cat.updated_at
        }

    async def create(self, data: CategoryCreate) -> AssetCategory:
        existing = await self.cat_repo.get_by_name(data.name)
        if existing:
            raise ConflictException("Category name already exists")
        return await self.cat_repo.create(data.model_dump())

    async def update(self, cat_id: UUID, data: CategoryUpdate) -> AssetCategory:
        cat = await self.cat_repo.get_by_id(cat_id)
        if not cat:
            raise NotFoundException("Category not found")
            
        if data.name and data.name != cat.name:
            existing = await self.cat_repo.get_by_name(data.name)
            if existing:
                raise ConflictException("Category name already exists")
                
        return await self.cat_repo.update(cat, data.model_dump(exclude_unset=True))
        
    async def delete(self, cat_id: UUID) -> None:
        cat = await self.cat_repo.get_by_id(cat_id)
        if not cat:
            raise NotFoundException("Category not found")
            
        # Hardcoded check: ideally we check assets table
        # asset_count = await self.cat_repo.get_asset_count(cat.id)
        asset_count = 0 
        if asset_count > 0:
            raise ConflictException("Cannot delete category with associated assets")
            
        await self.cat_repo.delete(cat)
