from fastapi import APIRouter
from app.routers.auth_router import router as auth_router
from app.routers.department_router import router as department_router
from app.routers.user_router import router as user_router
from app.routers.category_router import router as category_router
from app.routers.bookings import router as bookings_router
from app.routers.activity_logs import router as activity_logs_router
from app.routers.dashboard import router as dashboard_router
from app.routers.audits import router as audits_router
from app.routers.reports import router as reports_router

def register_routers(app):
    api_router = APIRouter(prefix="/api/v1")
    
    api_router.include_router(auth_router)
    api_router.include_router(department_router)
    api_router.include_router(user_router)
    api_router.include_router(category_router)
    api_router.include_router(bookings_router)
    api_router.include_router(activity_logs_router)
    api_router.include_router(dashboard_router)
    api_router.include_router(audits_router)
    api_router.include_router(reports_router)
    
    app.include_router(api_router)
