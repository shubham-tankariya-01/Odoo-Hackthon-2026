from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.dashboard import DashboardResponse
from app.controllers.dashboard_controller import DashboardController
from app.dependencies.database import get_db

from app.dependencies.auth import get_current_user

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard_route(current_user=Depends(
        get_current_user), db: AsyncSession = Depends(get_db)):
    """Fetch global KPIs and alerts for the operational dashboard."""
    return await DashboardController.get_dashboard(db)
