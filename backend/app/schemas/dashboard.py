from pydantic import BaseModel
from typing import List, Optional


class DashboardKPIs(BaseModel):
    assets_available: int
    assets_allocated: int
    maintenance_today: int
    active_bookings: int
    pending_transfers: int
    upcoming_returns: int
    overdue_returns: int


class DashboardReturnItem(BaseModel):
    allocation_id: str
    asset_tag: str
    asset_name: str
    employee_name: str
    expected_return_date: str
    days_overdue: Optional[int] = None
    days_until_due: Optional[int] = None


class DashboardResponse(BaseModel):
    kpis: DashboardKPIs
    overdue_returns: List[DashboardReturnItem]
    upcoming_returns: List[DashboardReturnItem]
