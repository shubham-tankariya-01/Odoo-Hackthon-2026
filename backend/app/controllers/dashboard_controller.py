from sqlalchemy.ext.asyncio import AsyncSession
from app.services.dashboard_service import DashboardService


class DashboardController:
    @staticmethod
    async def get_dashboard(db: AsyncSession):
        service = DashboardService(db)
        return await service.get_dashboard_stats()
