from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.booking import ResourceBooking
from app.schemas.dashboard import DashboardResponse, DashboardKPIs
from app.models.asset import Asset, AssetStatus
from app.models.maintenance import MaintenanceRequest
from app.models.transfer import Transfer, TransferStatus
from app.models.allocation import Allocation
from app.models.user import User
from datetime import datetime, date, timezone


class DashboardService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_dashboard_stats(self) -> DashboardResponse:
        # LIVE DATA: Count active bookings from our module
        result = await self.session.execute(
            select(func.count(ResourceBooking.id)).where(
                ResourceBooking.status == 'upcoming')
        )
        active_bookings_count = result.scalar() or 0

        today_date = date.today()

        # Count available assets
        result = await self.session.execute(select(func.count(Asset.id)).where(Asset.current_status == AssetStatus.available))
        assets_available_count = result.scalar() or 0

        # Count allocated assets
        result = await self.session.execute(select(func.count(Asset.id)).where(Asset.current_status == AssetStatus.allocated))
        assets_allocated_count = result.scalar() or 0

        # Count maintenance today (created_at >= start of today)
        # Note: simplistic date filtering for cross-db compat
        # Best would be >= datetime.combine(today_date, datetime.min.time())
        from datetime import time
        start_of_today = datetime.combine(
            today_date, time.min).replace(
            tzinfo=timezone.utc)
        result = await self.session.execute(
            select(func.count(MaintenanceRequest.id))
            .where(MaintenanceRequest.created_at >= start_of_today)
        )
        maintenance_today_count = result.scalar() or 0

        # Count pending transfers
        result = await self.session.execute(select(func.count(Transfer.id)).where(Transfer.status == TransferStatus.requested))
        pending_transfers_count = result.scalar() or 0

        # Count upcoming returns (due within 7 days, for example, and active)
        # Using simple python filtering or basic SQL for expected_return_date
        # >= today
        result = await self.session.execute(
            select(func.count(Allocation.id))
            .where(Allocation.is_active == True)
            .where(Allocation.expected_return_date >= today_date)
        )
        upcoming_returns_count = result.scalar() or 0

        # Count overdue returns
        result = await self.session.execute(
            select(func.count(Allocation.id))
            .where(Allocation.is_active == True)
            .where(Allocation.expected_return_date < today_date)
        )
        overdue_returns_count = result.scalar() or 0

        kpis = DashboardKPIs(
            assets_available=assets_available_count,
            assets_allocated=assets_allocated_count,
            maintenance_today=maintenance_today_count,
            active_bookings=active_bookings_count,
            pending_transfers=pending_transfers_count,
            upcoming_returns=upcoming_returns_count,
            overdue_returns=overdue_returns_count
        )

        # Overdue returns list (fetch real records)
        overdue_query = (
            select(Allocation, Asset.asset_tag, Asset.name.label(
                "asset_name"), User.name.label("employee_name"))
            .join(Asset, Allocation.asset_id == Asset.id)
            .join(User, Allocation.employee_id == User.id)
            .where(Allocation.is_active == True)
            .where(Allocation.expected_return_date < today_date)
            .limit(5)
        )
        overdue_result = await self.session.execute(overdue_query)

        overdue_returns = []
        for alloc, tag, asset_name, emp_name in overdue_result:
            days_overdue = (
                today_date -
                alloc.expected_return_date).days if alloc.expected_return_date else 0
            overdue_returns.append({
                "allocation_id": str(alloc.id),
                "asset_tag": tag,
                "asset_name": asset_name,
                "employee_name": emp_name,
                "expected_return_date": alloc.expected_return_date.isoformat() if alloc.expected_return_date else None,
                "days_overdue": days_overdue
            })

        # Upcoming returns list (fetch real records)
        upcoming_query = (
            select(Allocation, Asset.asset_tag, Asset.name.label(
                "asset_name"), User.name.label("employee_name"))
            .join(Asset, Allocation.asset_id == Asset.id)
            .join(User, Allocation.employee_id == User.id)
            .where(Allocation.is_active == True)
            .where(Allocation.expected_return_date >= today_date)
            .order_by(Allocation.expected_return_date.asc())
            .limit(5)
        )
        upcoming_result = await self.session.execute(upcoming_query)

        upcoming_returns = []
        for alloc, tag, asset_name, emp_name in upcoming_result:
            days_until_due = (
                alloc.expected_return_date -
                today_date).days if alloc.expected_return_date else 0
            upcoming_returns.append({
                "allocation_id": str(alloc.id),
                "asset_tag": tag,
                "asset_name": asset_name,
                "employee_name": emp_name,
                "expected_return_date": alloc.expected_return_date.isoformat() if alloc.expected_return_date else None,
                "days_until_due": days_until_due
            })

        return DashboardResponse(
            kpis=kpis,
            overdue_returns=overdue_returns,  # type: ignore
            upcoming_returns=upcoming_returns  # type: ignore
        )
