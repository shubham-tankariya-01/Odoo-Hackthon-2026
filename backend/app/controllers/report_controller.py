from fastapi import HTTPException
from fastapi.responses import Response
from typing import Optional
from app.services.report_service import ReportService

class ReportController:
    @staticmethod
    async def get_utilization(period: str, category_id: Optional[str] = None):
        service = ReportService()
        return await service.get_utilization(period, category_id)

    @staticmethod
    async def get_maintenance(period: str, group_by: Optional[str] = None):
        service = ReportService()
        return await service.get_maintenance(period, group_by)

    @staticmethod
    async def get_departments():
        service = ReportService()
        return await service.get_departments()

    @staticmethod
    async def get_bookings(period: str, asset_id: Optional[str] = None):
        service = ReportService()
        return await service.get_bookings(period, asset_id)

    @staticmethod
    async def get_retirement():
        service = ReportService()
        return await service.get_retirement()

    @staticmethod
    async def export_report(report_type: str, format: str, period: str):
        if format != "csv":
            raise HTTPException(status_code=400, detail="Only CSV format is supported at this time")
            
        service = ReportService()
        csv_data = await service.export_csv(report_type, period)
        
        filename = f"{report_type}_report_{period}.csv"
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
