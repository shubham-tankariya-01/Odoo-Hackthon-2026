from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.asset_category import AssetCategory
from app.repositories.base_repository import BaseRepository

class CategoryRepository(BaseRepository[AssetCategory]):
    def __init__(self, session: AsyncSession):
        super().__init__(AssetCategory, session)

    async def get_by_name(self, name: str) -> Optional[AssetCategory]:
        result = await self.session.execute(select(AssetCategory).where(AssetCategory.name == name))
        return result.scalars().first()
