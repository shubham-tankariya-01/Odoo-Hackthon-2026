import uuid
from typing import Optional, Sequence, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.models.asset import Asset
from app.repositories.base_repository import BaseRepository


class AssetRepository(BaseRepository[Asset]):
    def __init__(self, session: AsyncSession):
        super().__init__(Asset, session)

    async def get_by_tag(self, asset_tag: str) -> Optional[Asset]:
        result = await self.session.execute(
            select(Asset).where(Asset.asset_tag == asset_tag)
        )
        return result.scalars().first()

    async def get_by_serial(self, serial_number: str) -> Optional[Asset]:
        result = await self.session.execute(
            select(Asset).where(Asset.serial_number == serial_number)
        )
        return result.scalars().first()

    async def get_next_tag_number(self) -> int:
        """Return the next integer for the AF-XXXX sequence."""
        result = await self.session.execute(select(func.max(Asset.asset_tag)))
        max_tag: Optional[str] = result.scalar()
        if max_tag and max_tag.startswith("AF-"):
            try:
                return int(max_tag[3:]) + 1
            except ValueError:
                pass
        return 1

    async def search(
        self,
        asset_tag: Optional[str] = None,
        serial_number: Optional[str] = None,
        category_id: Optional[uuid.UUID] = None,
        current_status: Optional[str] = None,
        is_bookable: Optional[bool] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[Sequence[Asset], int]:
        query = select(Asset)

        if asset_tag:
            query = query.where(Asset.asset_tag.ilike(f"%{asset_tag}%"))
        if serial_number:
            query = query.where(Asset.serial_number.ilike(f"%{serial_number}%"))
        if category_id:
            query = query.where(Asset.category_id == category_id)
        if current_status:
            query = query.where(Asset.current_status == current_status)
        if is_bookable is not None:
            query = query.where(Asset.is_bookable == is_bookable)
        if search:
            query = query.where(
                or_(
                    Asset.name.ilike(f"%{search}%"),
                    Asset.asset_tag.ilike(f"%{search}%"),
                    Asset.serial_number.ilike(f"%{search}%"),
                )
            )

        # Total count
        count_result = await self.session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = count_result.scalar() or 0

        # Paginated results
        query = query.order_by(Asset.asset_tag).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all(), total
