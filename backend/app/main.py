from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.middleware.request_logger import RequestLoggerMiddleware

from app.routers import register_routers

def create_app() -> FastAPI:
    app = FastAPI(
        title="AssetFlow API",
        description="Enterprise Asset & Resource Management System",
        version="1.0.0",
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.parsed_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggerMiddleware)

    # Routers
    register_routers(app)

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "healthy"}

    return app

app = create_app()
