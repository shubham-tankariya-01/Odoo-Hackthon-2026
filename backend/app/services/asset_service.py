from typing import List, Tuple, Optional, Sequence
from uuid import UUID
from app.models.asset import Asset, AssetStatus, ALLOWED_TRANSITIONS
from app.repositories.asset_repo import AssetRepository
from app.schemas.asset import AssetCreate, AssetUpdate, AssetStatusUpdate
from app.utils.exceptions import (
    NotFoundException,
    ConflictException,
    ValidationException,
)


class AssetService:
    def __init__(self, repo: AssetRepository):
        self.repo = repo

    # ── Queries ──────────────────────────────────────

    async def get_all(
        self,
        asset_tag: Optional[str] = None,
        serial_number: Optional[str] = None,
        category_id: Optional[UUID] = None,
        current_status: Optional[str] = None,
        is_bookable: Optional[bool] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[Sequence[Asset], int]:
        return await self.repo.search(
            asset_tag=asset_tag,
            serial_number=serial_number,
            category_id=category_id,
            current_status=current_status,
            is_bookable=is_bookable,
            search=search,
            skip=skip,
            limit=limit,
        )

    async def get_by_id(self, asset_id: UUID) -> Asset:
        asset = await self.repo.get_by_id(asset_id)
        if not asset:
            raise NotFoundException("Asset not found")
        return asset

    # ── Mutations ─────────────────────────────────────

    async def create(self, data: AssetCreate) -> Asset:
        if data.serial_number:
            existing = await self.repo.get_by_serial(data.serial_number)
            if existing:
                raise ConflictException(
                    f"Serial number '{data.serial_number}' already registered"
                )

        next_num = await self.repo.get_next_tag_number()
        asset_tag = f"AF-{next_num:04d}"

        asset_in = {
            **data.model_dump(),
            "asset_tag": asset_tag,
            "current_status": AssetStatus.available,
        }
        return await self.repo.create(asset_in)

    async def update(self, asset_id: UUID, data: AssetUpdate) -> Asset:
        asset = await self.get_by_id(asset_id)

        if data.serial_number and data.serial_number != asset.serial_number:
            existing = await self.repo.get_by_serial(data.serial_number)
            if existing:
                raise ConflictException(
                    f"Serial number '{data.serial_number}' already in use"
                )

        update_dict = data.model_dump(exclude_unset=True)

        # Merge custom_fields instead of overwriting
        if "custom_fields" in update_dict and update_dict["custom_fields"]:
            merged = dict(asset.custom_fields or {})
            merged.update(update_dict["custom_fields"])
            update_dict["custom_fields"] = merged

        return await self.repo.update(asset, update_dict)

    async def change_status(self, asset_id: UUID, payload: AssetStatusUpdate) -> Asset:
        """
        Central state-machine gate.
        Every other module (allocations, maintenance, transfers) must call
        this instead of writing current_status directly.
        """
        asset = await self.get_by_id(asset_id)
        current = AssetStatus(asset.current_status)
        target = payload.status

        if target not in ALLOWED_TRANSITIONS.get(current, set()):
            raise ValidationException(
                f"Invalid transition: '{current}' → '{target}'"
            )

        return await self.repo.update(asset, {"current_status": target})

    async def dispose(self, asset_id: UUID) -> Asset:
        """Soft-delete via the state machine (sets status to 'disposed')."""
        asset = await self.get_by_id(asset_id)
        current = AssetStatus(asset.current_status)

        if AssetStatus.disposed not in ALLOWED_TRANSITIONS.get(current, set()):
            raise ConflictException(
                f"Cannot dispose asset in '{current}' status. "
                "Only 'available' and 'retired' assets can be disposed."
            )

        return await self.repo.update(asset, {"current_status": AssetStatus.disposed})
