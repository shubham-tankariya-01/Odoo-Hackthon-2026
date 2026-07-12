from fastapi import APIRouter
from app.routers.auth_router import router as auth_router
from app.routers.department_router import router as department_router
from app.routers.user_router import router as user_router
from app.routers.category_router import router as category_router
from app.routers.assets import router as asset_router
from app.routers.allocations import router as allocation_router
from app.routers.maintenance_router import router as maintenance_router

def register_routers(app):
    api_router = APIRouter(prefix="/api/v1")
    
    api_router.include_router(auth_router)
    api_router.include_router(department_router)
    api_router.include_router(user_router)
    api_router.include_router(category_router)
    api_router.include_router(asset_router)
    api_router.include_router(allocation_router)
    api_router.include_router(maintenance_router)
    
    app.include_router(api_router)
