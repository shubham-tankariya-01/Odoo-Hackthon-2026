from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.booking import ResourceBooking
from app.schemas.dashboard import DashboardResponse, DashboardKPIs

class DashboardService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_dashboard_stats(self) -> DashboardResponse:
        # LIVE DATA: Count active bookings from our module
        result = await self.session.execute(
            select(func.count(ResourceBooking.id)).where(ResourceBooking.status == 'upcoming')
        )
        active_bookings_count = result.scalar() or 0

        # MOCK DATA: Waiting for Members 1 & 2 to finish Asset, Allocation, and Maintenance models
        # FIXME: Replace hardcoded numbers with real repository counts once tables exist
        kpis = DashboardKPIs(
            assets_available=42,       # FIXME: Query Asset table where status == available
            assets_allocated=78,       # FIXME: Query Asset table where status == allocated
            maintenance_today=3,       # FIXME: Query MaintenanceRequest where date is today
            active_bookings=active_bookings_count,
            pending_transfers=5,       # FIXME: Query AssetTransfer
            upcoming_returns=8,        # FIXME: Query AssetAllocation where due soon
            overdue_returns=2          # FIXME: Query AssetAllocation where overdue
        )

        overdue_mock = [
            {
                "allocation_id": "al-001",
                "asset_tag": "AF-0114",
                "asset_name": "Laptop Dell XPS",
                "employee_name": "Raj Patel",
                "expected_return_date": "2026-07-01",
                "days_overdue": 11
            }
        ]

        upcoming_mock = [
            {
                "allocation_id": "al-002",
                "asset_tag": "AF-0032",
                "asset_name": "Projector Epson",
                "employee_name": "Priya Sharma",
                "expected_return_date": "2026-07-15",
                "days_until_due": 3
            }
        ]

        return DashboardResponse(
            kpis=kpis,
            overdue_returns=overdue_mock,
            upcoming_returns=upcoming_mock
        )
