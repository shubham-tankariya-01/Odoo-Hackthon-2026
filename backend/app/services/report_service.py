import io
import csv
from typing import Optional
from app.schemas.report import (
    UtilizationReport, MaintenanceReport, DepartmentReport, 
    BookingReport, RetirementReport, DepartmentReportItem
)

class ReportService:
    async def get_utilization(self, period: str, category_id: Optional[str] = None) -> UtilizationReport:
        # Mocking data until Asset & Allocation models are ready
        return UtilizationReport(
            period=period,
            total_assets=120,
            utilized_assets=78,
            utilization_rate=65.0,
            most_used=[
                { "asset_tag": "AF-0001", "name": "MacBook Pro 16\"", "allocation_days": 30 },
                { "asset_tag": "AF-0002", "name": "Conference Room B2 Projector", "booking_count": 45 }
            ],
            idle_assets=[
                { "asset_tag": "AF-0099", "name": "Old Scanner", "idle_days": 90 }
            ]
        )

    async def get_maintenance(self, period: str, group_by: Optional[str] = None) -> MaintenanceReport:
        # Mocking data until MaintenanceRequest model is ready
        return MaintenanceReport(
            period=period,
            total_requests=34,
            by_category=[
                { "category": "Electronics", "count": 22, "avg_resolution_days": 3.5 },
                { "category": "Vehicles", "count": 8, "avg_resolution_days": 7.2 },
                { "category": "Furniture", "count": 4, "avg_resolution_days": 2.1 }
            ],
            by_priority={
                "critical": 5,
                "high": 12,
                "medium": 10,
                "low": 7
            }
        )

    async def get_departments(self) -> DepartmentReport:
        # Mocking data until Asset & Allocation models are ready
        return DepartmentReport(
            departments=[
                DepartmentReportItem(
                    department_id="d5e6f7a8-1234-5678-1234-567812345678",
                    department_name="Engineering",
                    total_allocated=45,
                    total_employees=24,
                    assets_per_employee=1.88,
                    overdue_count=2
                ),
                DepartmentReportItem(
                    department_id="d9a8b7c6-1234-5678-1234-567812345678",
                    department_name="Marketing",
                    total_allocated=18,
                    total_employees=12,
                    assets_per_employee=1.5,
                    overdue_count=0
                )
            ]
        )

    async def get_bookings(self, period: str, asset_id: Optional[str] = None) -> BookingReport:
        # Mocking data, though we could query ResourceBooking here!
        return BookingReport(
            period=period,
            peak_hours=[
                { "hour": 9, "booking_count": 42 },
                { "hour": 10, "booking_count": 38 },
                { "hour": 14, "booking_count": 35 }
            ],
            peak_days=[
                { "day": "Monday", "booking_count": 28 },
                { "day": "Wednesday", "booking_count": 25 }
            ],
            most_booked_assets=[
                { "asset_tag": "AF-0002", "name": "Conference Room B2 Projector", "booking_count": 45 },
                { "asset_tag": "AF-0010", "name": "Meeting Room A1", "booking_count": 38 }
            ]
        )

    async def get_retirement(self) -> RetirementReport:
        # Mocking data until Asset model is ready
        return RetirementReport(
            nearing_retirement=[
                {
                    "asset_tag": "AF-0005",
                    "name": "Old Laptop ThinkPad",
                    "category": "Electronics",
                    "age_months": 58,
                    "maintenance_count": 8,
                    "current_status": "available",
                    "recommendation": "Consider retirement — high maintenance frequency"
                }
            ],
            already_retired=[
                {
                    "asset_tag": "AF-0003",
                    "name": "Broken Printer",
                    "current_status": "retired",
                    "retired_since": "2026-05-01"
                }
            ]
        )

    async def export_csv(self, report_type: str, period: str) -> str:
        # Generate dynamic CSV based on report_type
        output = io.StringIO()
        writer = csv.writer(output)
        
        if report_type == "utilization":
            writer.writerow(["Asset Tag", "Name", "Allocation Days", "Booking Count"])
            writer.writerow(["AF-0001", "MacBook Pro 16\"", "30", "0"])
            writer.writerow(["AF-0002", "Conference Room B2 Projector", "0", "45"])
        elif report_type == "maintenance":
            writer.writerow(["Category", "Request Count", "Avg Resolution Days"])
            writer.writerow(["Electronics", "22", "3.5"])
            writer.writerow(["Vehicles", "8", "7.2"])
        else:
            writer.writerow(["Report Type", "Period"])
            writer.writerow([report_type, period])
            
        return output.getvalue()
