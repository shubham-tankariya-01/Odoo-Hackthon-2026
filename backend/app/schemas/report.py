from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class UtilizationReport(BaseModel):
    period: str
    total_assets: int
    utilized_assets: int
    utilization_rate: float
    most_used: List[Dict[str, Any]]
    idle_assets: List[Dict[str, Any]]


class MaintenanceReport(BaseModel):
    period: str
    total_requests: int
    by_category: List[Dict[str, Any]]
    by_priority: Dict[str, int]


class DepartmentReportItem(BaseModel):
    department_id: str
    department_name: str
    total_allocated: int
    total_employees: int
    assets_per_employee: float
    overdue_count: int


class DepartmentReport(BaseModel):
    departments: List[DepartmentReportItem]


class BookingReport(BaseModel):
    period: str
    peak_hours: List[Dict[str, Any]]
    peak_days: List[Dict[str, Any]]
    most_booked_assets: List[Dict[str, Any]]


class RetirementReport(BaseModel):
    nearing_retirement: List[Dict[str, Any]]
    already_retired: List[Dict[str, Any]]
