from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.schemas.report import (
    UtilizationReport, MaintenanceReport, DepartmentReport,
    BookingReport, RetirementReport
)
from app.controllers.report_controller import ReportController

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/utilization", response_model=UtilizationReport)
async def get_utilization_report(period: str = Query("last_30_days"), category_id: Optional[str] = None, current_user=Depends(
        get_current_user), db: AsyncSession = Depends(get_db)):
    return await ReportController.get_utilization(db, period, category_id)


@router.get("/maintenance", response_model=MaintenanceReport)
async def get_maintenance_report(period: str = Query("last_90_days"), group_by: Optional[str] = None, current_user=Depends(
        get_current_user), db: AsyncSession = Depends(get_db)):
    return await ReportController.get_maintenance(db, period, group_by)


@router.get("/departments", response_model=DepartmentReport)
async def get_departments_report(current_user=Depends(
        get_current_user), db: AsyncSession = Depends(get_db)):
    return await ReportController.get_departments(db)


@router.get("/bookings", response_model=BookingReport)
async def get_bookings_report(period: str = Query("last_30_days"), asset_id: Optional[str] = None, current_user=Depends(
        get_current_user), db: AsyncSession = Depends(get_db)):
    return await ReportController.get_bookings(db, period, asset_id)


@router.get("/retirement", response_model=RetirementReport)
async def get_retirement_report(current_user=Depends(
        get_current_user), db: AsyncSession = Depends(get_db)):
    return await ReportController.get_retirement(db)


@router.get("/export")
async def export_report(report_type: str, format: str = Query("csv"), period: str = Query(
        "last_30_days"), current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ReportController.export_report(db, report_type, format, period)
