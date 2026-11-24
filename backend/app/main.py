from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.logging import get_logger

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application Lifespan Manager:
    Runs startup logic before yielding, and cleanup logic on shutdown.
    """
    logger.info(f"Starting {settings.PROJECT_NAME} in [{settings.ENVIRONMENT}] mode...")
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME} cleanly...")


# Initialize the FastAPI App with settings from config.py
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="1.0.0",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint: Returns service name and API documentation link."""
    return {
        "message": f"Welcome to {settings.SITE_NAME} API",
        "environment": settings.ENVIRONMENT,
        "docs_url": f"{settings.API_V1_STR}/docs",
    }


@app.get("/health", tags=["Health"])
@app.get(f"{settings.API_V1_STR}/health", tags=["Health"])
async def health_check():
    """Health check endpoint: Used by load balancers and container orchestrators."""
    logger.info("Health check endpoint pinged")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "project": settings.PROJECT_NAME,
        },
    )
